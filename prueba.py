i1 = 3
i2 = 6
padre = range(1,10)
madre = [9,3,7,8,2,6,5,1,4]
nCiudades = 10
hijo = [0]*(nCiudades-1) # inicia el hijo con el mismo valor en todo el array
if i1 < i2: i2 += 1     # normaliza: i1 siempre es menor que i2
else: i1, i2 = i2, i1+1 # 
hijo[i1:i2] = padre[i1:i2] # relleno el segmento en el hijo
tam = nCiudades-(i2-i1); # cuantos faltan para rellenar el hijo
x=i2; y=i2
for it in range(tam-1):
    if x == nCiudades-1: x=0 # empiezo desde el principio
    if y == nCiudades-1: y=0
    elem = madre[y]; y+=1
    if y == nCiudades-1: y=0
    while elem in hijo: # comprueba si esta ya en el hijo
        elem = madre[y]; y+=1;
        if y == nCiudades-1: y=0
    hijo[x] = elem; x+=1 # y lo introduce en el hijo
print hijo