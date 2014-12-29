#!/usr/bin/env python

# Bibliotecas de python
import random   # numeros aleatorios
import math     # operaciones matematicas
#import numpy    # otras operaciones matematicas

# Variables globales
nCiudades = 10  # Numero de ciudades
nPoblacion= 100 # Numero de soluciones en una poblacion
Pc = 0.9        # Probabilidad de cruce
Pm = 0.01       # Probabilidad de mutacion
distancias = {} # Diccionario de distancias
filedistancias = "distancias.txt"   # 
filealeatorios = "aleatorios.txt"   # Archivos
aleatorios = [] # lista de numeros aleatorios

# imprimir una lista sin comas ni nada
def imprimirLista(lista):
    print "0", # el 0 siempre es la primera ciudad
    for i in lista:
        print i,
    print "" # salto de linea al final

# lectura del fichero de distancias
def leerDistancias():
    i = 1;
    aux = []
    f = open(filedistancias, "r")
    for linea in f.readlines():
        aux = linea.split()
        distancias[i] = aux
        i += 1
    f.close()

# lectura del fichero de aleatorios
def leerAleatorios():
    global aleatorios; aleatorios = list() # reinicio la lista por si ya estaba llena
    f = open(filealeatorios, "r")
    for numero in f.readlines(): # guardo los numeros truncados en el array 
        aleatorios.append(float(numero))
    f.close()

# generacion de numeros aleatorios
def generarAleatorios():
    global aleatorios
    aleatorios = list()
    print " -> Implementar generacion aleatoria"
    #for i in range(nIteraciones*4):
    #    aleatorios.append(random.random())

# siguiente numero aleatorio para el torneo
def torneoAleatorio():
    global aleatorios
    return int(round(aleatorios.pop(0)*(nPoblacion-1)))

# siguiente numero aleatorio entero
def ciudadAleatoria():
    global aleatorios
    return int(round(aleatorios.pop(0)*(nCiudades-2)+1))

# siguiente numero aleatorio entre 0 y 1
def floatAleatorio():
    global aleatorios
    return aleatorios.pop(0)

# calcular la distancia entre dos ciudades
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
    aux = distancias[indices[nCiudades - 2]]
    total += int(aux[0])

    for i in range(len(indices) - 1):
        total += calcularDistancia(indices[i], indices[i + 1])
    return total

# el operador con el cual muta una solucion
def mutar(lista, a, b):
    lista[a], lista[b] = lista[b], lista[a] # intercambia los elementos

# obtener solucion aleatoria
def obtenerSolucionAleatoria():
    camino = []
    a = 0; i=0
    for i in range(nCiudades-1):
        a = ciudadAleatoria()
        while a in camino:
            a = ciudadAleatoria()
        camino.append(a);
    return camino

# obtener solucion voraz
def obtenerSolucionVoraz():
    camino = [] 
    actual = ciudadAleatoria(); menorD = 10000; menorI = 0
    camino.append(actual) # la primera ciudad es aleatoria
    for i in range(1,nCiudades-1):
        for j in range(1,nCiudades):
            if j not in camino and actual!=j:
                d = calcularDistancia(actual,j)
                if d < menorD:
                    menorD = d; menorI = j
        camino.append(menorI)
        actual = menorI;  menorI = -1; menorD = 1000000
    return camino

# obtener la solucion inicial (mitad voraz, mitad aleatoria)
def obtenerSolucionInicial():
    solucionInicial = []
    for i in range(nPoblacion/2): # soluciones aleatorias
        solucionInicial.append(obtenerSolucionAleatoria())
    for i in range(nPoblacion/2): # soluciones voraces
        solucionInicial.append(obtenerSolucionVoraz())
    print "POBLACION INICIAL"
    for i in range(len(solucionInicial)): # imprimir poblacion
        s = solucionInicial[i];  d = str(coste(s))
        print "INDIVIDUO",i,"= {OBJETIVO:",d+",","CAMINO:",
        imprimirLista(s),"}"
    return solucionInicial

# cuerpo principal del algoritmo
def algoritmo():
    return

leerDistancias()
leerAleatorios()
obtenerSolucionInicial()
