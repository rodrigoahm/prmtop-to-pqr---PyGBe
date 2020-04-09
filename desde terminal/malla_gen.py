import numpy
import os
import parmed.amber

#Dirección de MSMS, datos de entrada en .prmtop y .crd, dirección de salida
msms = '/home/rodrigo/codigo/msms.1'  #ubicación de MSMS
direccion_datos = '/home/rodrigo/Desktop/datos/'  #ubicación de moleculas a transformar
direccion_proteinas = '/home/rodrigo/Desktop/proteinas/'  #dirección a ubicar datos para pygbe

#Variables que se pueden modificar

#Elegir si utilizar Radio 'Born' (1) o Radio 'Lennard-Jones or VdW' (2)
OPCION = 1 #Valores 1 o 2

#Datos de entrada para MSMS:
radius_increase=0
p=1.4 #Probe Radius para generar SES
d=3.0 #densidad, valores usuales 1.0 (>1000) y 3.0 para moléculas mas pequeñas

#Parámetros para cambiar en .parm
NCRIT = 500
theta = 0.5

#Parámetros para cambiar en .config
eps = 1.5

#Listado de Moléculas:
lista_de_moleculas=[]
for dirpath ,dirnames, filenames in os.walk(direccion_datos):
    filenames
for molecula in filenames:
    if '.crd' in molecula:
        molecula=molecula[:-4]
        lista_de_moleculas.append(molecula)
    elif '.pqr' in molecula:
        molecula=molecula[:-4]
        lista_de_moleculas.append(molecula)

#Comenzar Ciclo:
for molecule_name in lista_de_moleculas:
    #Crear Carpeta:
    os.system('mkdir '+direccion_proteinas + molecule_name)
    #Definir variables para generar malla y pqr:
    dir_name = direccion_datos+molecule_name
    mol = parmed.amber.AmberParm(direccion_datos + molecule_name + '.prmtop')
    N_atom=mol.ptr('NATOM')
    nombre=mol.parm_data['ATOM_NAME']
    tipo=mol.parm_data['ATOM_TYPE_INDEX']
    carga=mol.parm_data['CHARGE']
    radio=numpy.zeros(N_atom)
    
    if OPCION == 1:
        radio[:] = mol.parm_data['RADII'][:]
            
    if OPCION == 2:
        for i in range(N_atom):
            radio[i] = mol.LJ_radius[tipo[i]-1] 
    
    
    if N_atom%2==0:
        mol_crd = numpy.loadtxt(direccion_datos+molecule_name+'.crd',skiprows=2)
        mol_crd.flatten()
        pos = numpy.reshape(mol_crd,(N_atom,3))
        
    elif N_atom%2!=0:
        maximas_filas=(N_atom-1)//2
        mol_crd=numpy.zeros(N_atom*3)
        mol_crd_ini= numpy.loadtxt(direccion_datos+molecule_name+'.crd',skiprows=2,max_rows=maximas_filas)
        mol_crd_end = numpy.loadtxt(direccion_datos+molecule_name+'.crd',skiprows=2+maximas_filas)
        mol_crd[N_atom*3-3:]=mol_crd_end[:]
        mol_crd[:N_atom*3-3]=mol_crd_ini.flatten()
        pos = numpy.reshape(mol_crd, (N_atom, 3))
        
    #Generar .pqr
    h=open(direccion_proteinas+molecule_name+'/'+molecule_name+'.pqr','w+')
    for i in range(N_atom):
        h.write('ATOM   %1.0f   %s   ALGO    %1.0f   %1.3f  %1.3f  %1.3f %1.4f %1.5f \n'%(i+1,nombre[i],tipo[i],pos[i][0],pos[i][1],pos[i][2],carga[i],radio[i])) 
    h.close()

    os.system('mkdir '+direccion_proteinas+'/'+molecule_name+'/geometry')
    xyzr_data = numpy.zeros((N_atom,4))
    xyzr_data[:,:3] = pos[:,:]
    xyzr_data[:,-1] = radio[:] + radius_increase
    #Generar .xyzr y Malla.
    dir_x_molec = direccion_proteinas+molecule_name
    dir_x_molec_name=dir_x_molec+'/'+molecule_name
    
    numpy.savetxt(dir_x_molec_name+'.xyzr',xyzr_data)
    cmd = msms+' -if '+dir_x_molec_name+'.xyzr -of '+dir_x_molec+'/geometry/'+\
    molecule_name + (' -d %1.1f -p %1.1f -no_header') %(d,p)
    os.system(cmd)
    
    #Generar .param
    f=open(direccion_proteinas+molecule_name+'/'+molecule_name+'.param','w+')
    text_param = 'Precision   double\n\
K           4\n\
Nk          9\n\
K_fine      37\n\
thresold    0.5\n\
BSZ         128\n\
restart     100\n\
tolerance   1e-6\n\
max_iter    1000\n\
P           8\n\
eps         1e-12\n\
NCRIT       %1.0f\n\
theta       %1.2f\n\
GPU         0\n\
polar_eps   1e-2'%(NCRIT, theta)
    f.write(text_param)
    f.close()
    
    #Generar .config
    g=open(direccion_proteinas+molecule_name+'/'+molecule_name+'.config','w+')
    config_text = \
    'FILE    geometry/MOLECULE    dielectric_interface\n\
--------------------------------\n\
PARAM   LorY E?   Dielec  kappa   charges?    coulomb?  charge_file     Nparent parent  Nchild  children\n\
FIELD   1    0      80    1e-12       0           0       NA              0       NA      1       0\n\
FIELD   1    1      %1.2f   1e-12       1           1       MOLECULE        1       0       0       NA'\
    %(eps)
    config_text_mod1=config_text.replace('geometry/MOLECULE','geometry/'+molecule_name)
    config_text_mod2=config_text_mod1.replace('MOLECULE',molecule_name+'.pqr')
    g.write(config_text_mod2)
    g.close()
    
    
