#!/usr/bin/env python

# Bibliotecas
import random
import math

# Variables globales
n = 100  # Numero de ciudades
nEjecuciones = 10  # numero de ejecuciones del algoritmo
nIteraciones = 10000 # numero de iteraciones dentro del algoritmo
distancias = {}  # diccionario para guardar las distancias entre las ciudades cargado del fichero
filein = "distancias_100ciudades.txt"
filealeatorios = "aleatorios.txt"
aleatorios = [] # lista de indices aleatorios

# lectura del fichero y carga de datos
def leerfichero():
    i = 1;
    aux = []
    f = open(filein, "r")
    for linea in f.readlines():
        aux = linea.split()
        distancias[i] = aux
        i += 1
    # print distancias
    f.close()

# lectura del fichero de numeros aleatorios o generacion de los mismos
def leerAleatorios(confichero):
    global aleatorios
    aleatorios = list() # reinicio la lista por si ya estaba llena
    if confichero:
        f = open(filealeatorios, "r")
        for numero in f.readlines(): # guardo los numeros truncados en el array
            aleatorios.append( 1 + int(math.floor(float(numero)*(n-1))) )
        f.close()
    else:
        for numero in range(0,10000):
            aleatorios.append(random.randrange(1,n))

# calcula la distancia entre dos ciudades
def calcularDistancia(ciudad1, ciudad2):
    d = 0
    if ciudad1 < ciudad2:
        array = distancias[ciudad2]
        d = int(array[ciudad1])
    elif ciudad1 > ciudad2:
        array = distancias[ciudad1]
        d = int(array[ciudad2])
    else:
        print " -> Error al calcular la distancia: indices iguales"
    return d

# calcular la distancia total de una solucion
def calcularDistanciaTotal(indices):
    i = 0;
    total = 0;
    # sumo al total la distancia de 0 a 1
    aux = distancias[indices[0]]
    total += int(aux[0])
    # sumo al total la distancia de 0 a n-1
    aux = distancias[indices[n - 2]]
    total += int(aux[0])

    for i in range(len(indices) - 1):
        total += calcularDistancia(indices[i], indices[i + 1])
    return total

# intercambiar dos elementos de la lista
def operadorPosicion(lista, origen, destino):
    vecino = list(lista)
    vecino.insert( destino , vecino.pop(origen) )
    return vecino

# generar lista con los vecinos de una solucion
def generarVecinos(tabu, ciudades, indice):
    vecinos = []
    for i in range(len(ciudades)):
        if i != indice:
            aux = operadorPosicion(ciudades, indice, i) 
            if getTerna(aux, aux[i]) not in tabu: # solo generamos los vecinos que no estan en la lista tabu
                vecinos.append([aux,i]) # guardo el vecino y el indice que lo genera
    return vecinos

# obtener la solucion inicial con una estrategia voraz
def obtenerSolucionInicial():
    solucionInicial = []
    menorD = 10000
    menorI = 0

    for i in range(0,n-1):
        actual = menorI
        menorI = -1
        menorD = 1000000
        for j in range(1,n):
            if j not in solucionInicial and actual!=j:
                d = calcularDistancia(actual,j)
                if d < menorD:
                    menorD = d
                    menorI = j
        solucionInicial.append(menorI)
    return solucionInicial

# devuelve la terna resultante del intercambio de una ciudad
def getTerna(ciudades, ciudad):
    posicion = ciudades.index(ciudad)
    if posicion == 0:
        return [0,ciudades[posicion],ciudades[posicion+1]]
    elif posicion == n-2:
        return [ciudades[posicion-1],ciudades[posicion],0]
    else:
        return [ciudades[posicion-1],ciudades[posicion],ciudades[posicion+1]]

# algoritmo de busqueda tabu
def algoritmo(op):
    solucionActual = obtenerSolucionInicial()
    if op != "s":
        leerAleatorios(False) # recargo el array de aleatorios
    ciudadesAleatorias = list(aleatorios)
    siguienteVecino = list(solucionActual)
    mejorVecino = list(solucionActual)
    mejorDistancia = calcularDistanciaTotal(solucionActual)
    tabu = []; contador100 = -1; nReinicios = 0; mejorI = 0

    #print "RECORRIDO INICIAL:",solucionActual
    #print "DISTANCIA:",mejorDistancia,"\n"

    for i in range(nIteraciones):
        contador100+=1
        if (contador100==100):
            contador100 = 0; nReinicios+=1; tabu = []
            #print "========= REINICIO",nReinicios,"========="
            solucionActual = list(mejorVecino)
        else:
            solucionActual = list(siguienteVecino)
        ciudad = ciudadesAleatorias.pop(0) # saco el primer elemento aleatorio y miro donde esta en el array
        indice = solucionActual.index(ciudad)
        vecinos = generarVecinos(tabu, solucionActual, indice)
        d = calcularDistanciaTotal(solucionActual)
        #print "ITERACION:",i+1
        #print "CIUDAD A CAMBIAR:",ciudad
        #print "POSICIONES CONSIDERADAS: ",
        # primera posicion
        menor = calcularDistanciaTotal(vecinos[0][0]);
        #print "0",
        siguienteVecino = list(vecinos[0][0])
        solucionActual = list(vecinos[0][0])
        # siguientes posiciones
        for vecinoAux in vecinos:
            dist = calcularDistanciaTotal(vecinoAux[0])
            if dist < menor:
                solucionActual = list(vecinoAux[0])
                menor = dist
                siguienteVecino = list(vecinoAux[0])
                #print vecinoAux[1], # el segundo campo guarda el indice que cambio
                if dist < mejorDistancia: # cada 100 iteraciones compruebo si hay un vecino mejor
                    mejorDistancia = dist
                    mejorI = i+1 # mejor iteracion
                    mejorVecino = list(vecinoAux[0])
                    contador100 = -1; # reinicio el contador
                    #print "\n========= RECORRIDO MEJOR SOLUCION GLOBAL ========="

        #print "\nSOLUCION ACTUAL: ",siguienteVecino
        #print "DISTANCIA: ",menor
        tabu.append(getTerna(siguienteVecino,ciudad))
        #print "TABU:",tabu,"\n\n"
    #print "\nMejor distancia:",mejorDistancia
    #print "\nMejor vecino:",mejorVecino
    #print "\nEn la iteracion:",mejorI
    #print "Numero de reinicios:",nReinicios
    return mejorDistancia,mejorVecino,mejorI,nReinicios

# Ejecucion
leerfichero()
print "Desea usar el archivo 'aleatorios.txt'? (s/n):",
opcion = raw_input()
opcion = opcion.lower()
if opcion == "s":
    leerAleatorios(opcion)
solucionInicial = obtenerSolucionInicial()
algoritmo(opcion)

mejorD,mejorV,mejorI,mejorR=algoritmo(opcion)
peorD = 0; dist = list(); iterac = list(); reinic = list()
mediaD=mejorD; mediaI=mejorI; mediaR=mejorR;
for ejecucion in range(nEjecuciones-1):
    D,V,I,R=algoritmo(opcion)
    mediaD+=float(D); mediaI+=float(I); mediaR+=float(R);
    dist.append(D)   # arrays para la desviacion estandar
    iterac.append(I) #
    reinic.append(R) #
    if D < mejorD:
        mejorD = D
        mejorV = V
        mejorI = I
        mejorR = R
    if D > peorD:
        peorD = D

print "-------- MEJOR SOLUCION --------"
print "Distancia Minima:",mejorD
print "Mejor solucion:",mejorV
print "Mejor iteracion:",mejorI
print "Numero reinicios:",mejorR
mediaD/=nEjecuciones; mediaI/=nEjecuciones; mediaR/=nEjecuciones
print "--------- ESTADISTICAS ---------"
print "Distancia Maxima:",peorD
print "Distancia Media:",mediaD
#desviacion = math.sqrt((sum([x * x for x in dist]) / nEjecuciones) - (mediaD ** 2))
#print "Distancia Desviacion:",desviacion
print "Iteraciones Media:",mediaI
#desviacion = math.sqrt((sum([x * x for x in iterac]) / nEjecuciones) - (mediaI ** 2))
#print "Iteraciones Desviacion:",desviacion
print "Reinicios Media:",mediaR
#desviacion = math.sqrt((sum([x * x for x in reinic]) / nEjecuciones) - (mediaR ** 2))
#print "Reinicios Desviacion",desviacion
