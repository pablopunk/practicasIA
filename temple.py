#!/usr/bin/env python

# Bibliotecas
import random
import math

# Variables globales
n = 100  # Numero de ciudades
nEjecuciones = 10  # numero de ejecuciones del algoritmo
nIteraciones = 10 # numero de iteraciones dentro del algoritmo
distancias = {}  # diccionario para guardar las distancias entre las ciudades cargado del fichero
filein = "distancias.txt"
filealeatorios = "aleatorios.txt"
aleatorios = [] # lista de indices aleatorios
e=2.718281828459045 # numero de euler
mu=0.03  # constantes para la formula
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

# lectura del fichero de numeros aleatorios o generacion de los mismos
def leerAleatorios(confichero):
    global aleatorios
    aleatorios = list() # reinicio la lista por si ya estaba llena
    if confichero:
        f = open(filealeatorios, "r")
        for numero in f.readlines(): # guardo los numeros truncados en el array
            aleatorios.append(float(numero))
        f.close()
    else:
    	for numero in range(0,nIteraciones):
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
    Tactual = (mu / -math.log(phi,e)) * costeActual

    print "RECORRIDO INICIAL\n",recorridoActual
    print "FUNCION OBJETIVO:",costeActual
    print "TEMPERATURA:",Tactual,"\n"

    for iteracion in range(nIteraciones):
        ciudad = siguienteIntAleatorio()
        indice = siguienteIntAleatorio()-1
        print "ITERACION:",iteracion+1
        print "RANDOM CIUDAD:",ciudad,"| RANDOM INDICE INSERCION:",indice,"\n"
        recorridoNuevo = operadorPosicion(recorridoActual,recorridoActual.index(ciudad), indice)
        costeNuevo = coste(recorridoNuevo)
        delta = costeNuevo - costeActual
        aleatorio = siguienteFloatAleatorio()
        print recorridoNuevo
        print "DELTA:",delta
        print "RANDOM U[0, 1):",aleatorio 

# Ejecucion
leerfichero()
leerAleatorios(1)
algoritmo()
