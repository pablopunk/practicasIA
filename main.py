#!/usr/bin/env python

# Bibliotecas
import random
import itertools
import sys
import math
import os 

# Variables globales
n = 10  # Numero de ciudades
nIteraciones = 10  # numero de ejecuciones del algoritmo
distancias = {}  # diccionario para guardar las distancias entre las ciudades cargado del fichero
filein = "distancias_test.txt"
filealeatorios = "aleatorios_test.txt"
vecinoinicial = [] # del fichero de aleatorios
aleatorios = [] # numeros aleatorios (permutaciones de 2 elementos)

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
    hayAleatorios = True
    f = open(filealeatorios, "r")
    count = 0
    while count < n-1: # busca la solucion inicial hasta que las ciudades son diferentes
        numero = f.readline()
        num = 1+int(math.floor(float(numero)*(n-1)))
        if num not in vecinoinicial:
            vecinoinicial.append(num)
            vecinoinicial[count] = num
            count+=1
    count = 0
    for numero in f.readlines(): # permutaciones
        num = int(math.floor(float(numero)*(n-1)))
        aleatorios.append(num)

# calcular la distancia total
def calcularDistancia(indices):
    i = 0;
    total = 0; d = 0
    # sumo al total la distancia de 0 a 1
    aux = distancias[indices[0]]
    total += int(aux[0])
    # sumo al total la distancia de 0 a n-1
    aux = distancias[indices[n - 2]]
    total += int(aux[0])

    for i in range(len(indices) - 1):
        aux = indices[i]
        aux1 = indices[i + 1]
        if aux1 < aux:
            array = distancias[aux]
            d = int(array[aux1])
        elif aux1 > aux:
            array = distancias[aux1]
            d = int(array[aux])
        # print "Distancia entre %d y %d: %d" % (aux,aux1,d)
        total += d
    return total


# intercambiar dos elementos de la lista
def intercambiar(lista, a, b):
    aux = lista[a]
    lista[a] = lista[b]
    lista[b] = aux

# funcion principal del algoritmo
def algoritmo():
    vecinoactual = range(1, n)  # array de posiciones de las ciudades
    mejorvecino = []
    aux = []
    permutaciones = []
    numeroSolucion = 0

    if not hayAleatorios(): # si la lista aleatorios esta vacia
        random.shuffle(vecinoactual) # posiciones aleatorias
        permutaciones = list(itertools.permutations(range(0, n - 1), 2)) # todas las posibles permutaciones
    else:
        vecinoactual = vecinoinicial[:]
        for i in xrange(0,len(aleatorios)-1,2):
            permutaciones.append([aleatorios[i],aleatorios[i+1]])

    print vecinoactual

    while True:
        mejorvecino = list(vecinoactual)  # copio el vecino actual
        aux = []
        vecinos = []
        cuenta = 0; dist = 0

        if not hayAleatorios():
            random.shuffle(permutaciones)  # orden aleatorio de las permutaciones

        print "------- Solucion",numeroSolucion,"-------"; numeroSolucion+=1
        print "Camino: ",mejorvecino
        print "Distancia: ",calcularDistancia(mejorvecino)

        # recorro todas las permutaciones posibles hasta que encuentre una distancia menor
        for i in range(0, len(permutaciones)):
            aux = list(vecinoactual)
            # prueba la permutacion
            permutacion = permutaciones.pop(0)
            a = permutacion[0]
            b = permutacion[1]
            intercambiar(aux, a, b)
            if aux in vecinos or (a==b):
                continue # paso a la siguiente iteracion
            vecinos.append(aux) # llevo un array de vecinos para comprobar que no se repiten
            dist = calcularDistancia(aux)
            # imprimo cada vecino
            print "   ----- Vecino %d -----" % cuenta; cuenta+=1
            print "   [",a,"<->",b,"]"
            print "  ",aux
            print "  ","Distancia: ",dist
            if dist < calcularDistancia(mejorvecino):
                break

        if dist < calcularDistancia(vecinoactual):
            vecinoactual = list(aux)

        if dist >= calcularDistancia(mejorvecino):
            break

    #print "Distancia actual: %d" % calcularDistancia(vecinoactual)
    return vecinoactual, calcularDistancia(vecinoactual)


# escribe los resultados del algoritmo varias veces
def imprimir(iteraciones):
    media = 0;
    dist = list()  # voy a calcular la media y la desviacion
    menor = 1000000000;
    mayor = 0
    for i in range(1, iteraciones + 1):
        solucion, distanciaTotal = algoritmo()
        media += distanciaTotal
        if distanciaTotal < menor:
            menor = distanciaTotal
        if distanciaTotal > mayor:
            mayor = distanciaTotal
        dist.append(distanciaTotal)
        print "\nSolucion %d:" % i
        print solucion
        print "Distancia: %d KM\n" % distanciaTotal

    # Media y desviacion
    media /= iteraciones
    desviacion = math.sqrt((sum([x * x for x in dist]) / iteraciones) - (media ** 2))
    print "Media = %d\tDesviacion = %.2f" % (media, desviacion)
    print "Menor = %d\tMayor = %d\n" % (menor, mayor)

def hayAleatorios():
    if len(sys.argv) > 1 and os.path.isfile(filealeatorios):
        return True
    return False

def main():
    leerfichero()  # cargo los datos
    if hayAleatorios():
        print "Usando el fichero " + str(filealeatorios)
        leerAleatorios()
        imprimir(1)  # imprimo n iteraciones del algoritmo
    elif len(sys.argv) > 1:
        print " -> python main.py aleatorios.txt"
    else:
        imprimir(nIteraciones)  # imprimo n iteraciones del algoritmo


if __name__ == '__main__':  # funcion main en el archivo main
    main()
