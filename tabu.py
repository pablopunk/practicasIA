#!/usr/bin/env python

# Bibliotecas
import random
import itertools
import sys
import math
import os

# Variables globales
n = 100  # Numero de ciudades
nIteraciones = 10  # numero de ejecuciones del algoritmo
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

# lectura del fichero de numeros aleatorios
def leerAleatorios():
    f = open(filealeatorios, "r")
    for numero in f.readlines(): # guardo los numeros truncados en el array
        aleatorios.append( int(math.floor(float(numero)*(n-1))) )

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
def generarVecinos(ciudades, indice):
    vecinos = []
    for i in range(len(ciudades)):
        if i != indice:
            vecinos.append( operadorPosicion(ciudades, indice, i) )

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

# Ejecucion
leerfichero()
print obtenerSolucionInicial()
