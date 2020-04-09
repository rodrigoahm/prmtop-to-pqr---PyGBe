import os

#Dirección de MSMS, datos de entrada en .prmtop y .crd, dirección de salida
direccion_proteinas = '/home/rodrigo/Desktop/proteinas/'  #dirección a ubicar datos para pygbe
lista_de_moleculas=[]
for dirpath ,dirnames, filenames in os.walk(direccion_proteinas):
    filenames
    for molecula in filenames:
        if '.pqr' in molecula:
                molecula=molecula[:-4]
                lista_de_moleculas.append(molecula)

for molecula in lista_de_moleculas:
    os.system( 'pygbe ' + direccion_proteinas+molecula)
