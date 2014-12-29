#!/usr/bin/env python

# Bibliotecas de python
import random   # numeros aleatorios
import math     # operaciones matematicas
import numpy    # otras operaciones matematicas

# Variables globales
nCiudades = 10  # Numero de ciudades
nPoblacion= 100 # Numero de soluciones en una poblacion
Pc = 0.9        # Probabilidad de cruce
Pm = 0.01       # Probabilidad de mutacion
distancias = {} # Diccionario de distancias
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
    aux = distancias[indices[n - 2]]
    total += int(aux[0])

    for i in range(len(indices) - 1):
        total += calcularDistancia(indices[i], indices[i + 1])
    return total

# el operador con el cual muta una solucion
def mutar(lista, a, b):
    lista[a], lista[b] = lista[b], lista[a] # intercambia los elementos

# obtener la solucion inicial (mitad voraz, mitad aleatoria)


