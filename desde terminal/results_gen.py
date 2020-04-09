import os
from datetime import datetime 
direccion_proteinas = '/home/rodrigo/Desktop/proteinas/' 

lista_moleculas=[]
for dirpath, dirnames, filenames in os.walk(direccion_proteinas):
    for molecula in filenames:
        if '.pqr' in molecula:
            lista_moleculas.append(molecula[:-4])
            
g=open(direccion_proteinas+'resultados '+str(datetime.now())[:-7]+'.txt','w+')
for name in lista_moleculas:
    logs=[]
    c=0
    for a,b, filenames in os.walk(direccion_proteinas+name+'/output'):
        for log in filenames:
            if '.log' in log:
                logs.append(log)
    f=open(direccion_proteinas+name+'/output/'+logs[-1])
    E_solv=[]
    while(True):
        linea=f.readline()
        if 'E_solv = ' in linea:
            E_solv.append(linea)
            
        if not linea:
            break
    f.close()
    os.system('mv ' +direccion_proteinas+name+'/output/'+logs[-1] + ' ' + direccion_proteinas+name+'/output/'+logs[-1][:-4]+'.revisado')
    del logs
    if E_solv!=0:
        g.write(name+'   '+E_solv[-1])
    del E_solv
    
    
g.close()
