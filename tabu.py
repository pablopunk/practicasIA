#!/usr/bin/env python
## Se recomienda usar un compilador de python para aumentar la eficiencia

# Bibliotecas
import random
import itertools
import sys
import math
import os

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
def leerAleatorios(hayFichero):
    if hayFichero:
        f = open(filealeatorios, "r")
        for numero in f.readlines(): # guardo los numeros truncados en el array
            aleatorios.append( 1 + int(math.floor(float(numero)*(n-1))) )
    else:
        for numero in range(0,10000):
            aleatorios.append(random.random(1,n))

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
            if getTerna(aux, aux[indice]) not in tabu: # solo generamos los vecinos que no estan en la lista tabu
                vecinos.append(aux)
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
def algoritmo():
    solucionActual = obtenerSolucionInicial()
    ciudadesAleatorias = list(aleatorios)
    siguienteVecino = list(solucionActual)
    mejorVecino = list(solucionActual)
    mejorDistancia = calcularDistanciaTotal(solucionActual)
    tabu = []; contador100 = -1; nReinicios = 0; mejorI = 0

    print "RECORRIDO INICIAL:",solucionActual
    print "DISTANCIA:",mejorDistancia,"\n"

    for i in range(nIteraciones):
        contador100+=1
        if (contador100==100):
            contador100 = 0; nReinicios+=1; tabu = []
            print "========= REINICIO",nReinicios,"========="
            solucionActual = list(mejorVecino)
        else:
            solucionActual = list(siguienteVecino)
        ciudad = ciudadesAleatorias.pop(0) # saco el primer elemento aleatorio y miro donde esta en el array
        indice = solucionActual.index(ciudad)
        vecinos = generarVecinos(tabu, solucionActual, indice)
        d = calcularDistanciaTotal(solucionActual)
        print "ITERACION:",i+1
        print "CIUDAD A CAMBIAR:",ciudad
        print "POSICIONES CONSIDERADAS: ",
        # primera posicion
        menor = calcularDistanciaTotal(vecinos[0]);
        print "0",
        siguienteVecino = list(vecinos[0])
        solucionActual = list(vecinos[0])
        # siguientes posiciones
        for j in range(1,len(vecinos)):
            vecinoAux = vecinos[j]
            dist = calcularDistanciaTotal(vecinoAux)
            if dist < menor:
                solucionActual = list(vecinoAux)
                menor = dist
                siguienteVecino = list(vecinoAux)
                print j,
                if dist < mejorDistancia: # cada 100 iteraciones compruebo si hay un vecino mejor
                    mejorDistancia = dist
                    mejorI = i+1 # mejor iteracion
                    mejorVecino = list(vecinoAux)
                    contador100 = -1; # reinicio el contador
                    print "\n========= RECORRIDO MEJOR SOLUCION GLOBAL =========\n"

        print "\nSOLUCION ACTUAL: ",siguienteVecino
        print "DISTANCIA: ",menor
        tabu.append(getTerna(siguienteVecino,ciudad))
        print "TABU:",tabu,"\n"
    print "\nMejor distancia:",mejorDistancia
    print "En la iteracion:",mejorI
    print "Numero de reinicios:",nReinicios

# Ejecucion
leerfichero()
leerAleatorios(True)
solucionInicial = obtenerSolucionInicial()
algoritmo()