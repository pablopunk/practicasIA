#!/usr/bin/env python

# Bibliotecas
import random
import math
import numpypy
import numpy

# Variables globales
n = 100  # Numero de ciudades
nEjecuciones = 10  # numero de ejecuciones del algoritmo
nIteraciones = 10000 # numero de iteraciones dentro del algoritmo
distancias = {}  # diccionario para guardar las distancias entre las ciudades cargado del fichero
filein = "distancias.txt"
filealeatorios = "aleatorios.txt"
aleatorios = [] # lista de indices aleatorios
mu=0.25  # constantes para la formula
phi=0.99 # 

# lectura del fichero y carga de datos
def leerfichero():
    i = 1;
    aux = []
    f = open(filein, "r")
    for linea in f.readlines():
        aux = linea.split()
        distancias[i] = aux
        i += 1
    # print distancia
    f.close()

# siguiente numero aleatorio entero
def siguienteIntAleatorio():
    return 1+int(math.floor(aleatorios.pop(0)*(n-1)))

# siguiente numero aleatorio entre 0 y 1
def siguienteFloatAleatorio():
    return aleatorios.pop(0)

# lectura del fichero de aleatorios
def leerAleatorios():
    global aleatorios
    aleatorios = list() # reinicio la lista por si ya estaba llena

    f = open(filealeatorios, "r")
    for numero in f.readlines(): # guardo los numeros truncados en el array 
        aleatorios.append(float(numero))
    f.close()

# generacion de numeros aleatorios
def generarAleatorios():
    global aleatorios
    aleatorios = list()
    for i in range(nIteraciones*4):
        aleatorios.append(random.random())

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
def coste(indices):
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

# obtener la solucion inicial con una estrategia voraz
def obtenerSolucionInicial():
    solucion = []
    menorD = 10000
    menorI = 0

    for i in range(0,n-1):
        actual = menorI
        menorI = -1
        menorD = 1000000
        for j in range(1,n):
            if j not in solucion and actual!=j:
                d = calcularDistancia(actual,j)
                if d < menorD:
                    menorD = d
                    menorI = j
        solucion.append(menorI)
    return solucion

# algoritmo de busqueda tabu
def algoritmo():
    recorridoActual = obtenerSolucionInicial()
    costeActual = coste(recorridoActual)
    mejorSolucion = list(recorridoActual)
    mejorIteracion = 0; mejorDistancia = costeActual; aceptadas=0
    T0 = (mu / -math.log1p(phi-1)) * costeActual
    Tnuevo = T0
    contador80=1; contador20=0; nEnfriamientos=0
    #print "RECORRIDO INICIAL\n",recorridoActual
    #print "FUNCION OBJETIVO:",costeActual
    #print "TEMPERATURA:",T0,"\n"

    for iteracion in range(nIteraciones):
        ciudad = siguienteIntAleatorio()
        origen = recorridoActual.index(ciudad)
        destino = siguienteIntAleatorio()-1
        while destino == origen: # cojo el siguiente destino pero que no sea el mismo de la ciudad
            destino = siguienteIntAleatorio()-1
        #print "ITERACION:",iteracion+1
        #print "RANDOM CIUDAD:",ciudad,"| RANDOM INDICE INSERCION:",destino,"\n"
        recorridoNuevo = operadorPosicion(recorridoActual,origen,destino)
        costeNuevo = coste(recorridoNuevo)
        delta = costeNuevo - costeActual
        aleatorio = siguienteFloatAleatorio()
        #print recorridoNuevo
        #print "FUNCION OBJETIVO:",costeNuevo
        #print "DELTA:",delta
        #print "RANDOM U[0, 1):",aleatorio
        if (delta < 0) or (aleatorio < math.exp(-delta/Tnuevo)):
            recorridoActual = list(recorridoNuevo)
            costeActual = costeNuevo
            #print "SOLUCION CANDIDATA ACEPTADA"
            contador20+=1; aceptadas+=1
            if costeActual < mejorDistancia:
                mejorIteracion = iteracion+1
                mejorDistancia = costeActual
                mejorSolucion = list(recorridoActual)
        if contador80>=80 or contador20>=20:
            #print "** VELOCIDAD DE ENFRIAMIENTO ALCANZADA **"
            #print "CANDIDATAS",contador80,"| ACEPTADAS",contador20
            nEnfriamientos+=1
            #print "================="
            #print "ENFRIAMIENTO:",nEnfriamientos
            #print "================="
            contador80=0; contador20=0;
            Tnuevo = T0 / (nEnfriamientos+1)
            #print "TEMPERATURA:",Tnuevo
        contador80+=1; #print "\n"
    return mejorSolucion,aceptadas
# Ejecucion
leerfichero()
aceptadas = []; mejor = []
for i in range(nEjecuciones):
    generarAleatorios()
    mejor,ac=algoritmo()
    aceptadas.append(ac)
print "--- CANDIDATAS ACEPTADAS ---"
print "media:",numpy.mean(aceptadas)
print "desviacion:",numpy.std(aceptadas)
print "--- MEJOR SOLUCION ---"
print "distancia:",coste(mejor)
