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
cuentaAleatorios = 0

# imprimir una lista sin comas ni nada
def imprimirLista(lista):
    print "0", # el 0 siempre es la primera ciudad
    for i in lista:
        print i,

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
    global aleatorios,cuentaAleatorios
    al = int(round(aleatorios[cuentaAleatorios]*(nPoblacion-1)))
    cuentaAleatorios+=1
    return al

# siguiente numero aleatorio entero
def ciudadAleatoria():
    global aleatorios,cuentaAleatorios
    al = int(round(aleatorios[cuentaAleatorios]*(nCiudades-2)+1))
    cuentaAleatorios+=1
    return al

# siguiente numero aleatorio entre 0 y 1
def floatAleatorio():
    global aleatorios,cuentaAleatorios
    al = aleatorios[cuentaAleatorios]
    cuentaAleatorios+=1
    return al

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
    return lista

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
def obtenerpoblacioninicial():
    poblacioninicial = []
    for i in range(nPoblacion/2): # soluciones aleatorias
        poblacioninicial.append(obtenerSolucionAleatoria())
    for i in range(nPoblacion/2): # soluciones voraces
        poblacioninicial.append(obtenerSolucionVoraz())
    print "POBLACION INICIAL"
    for i in range(len(poblacioninicial)): # imprimir poblacion
        s = poblacioninicial[i];  d = str(coste(s))
        print "INDIVIDUO",i,"= {OBJETIVO:",d+",","CAMINO:",
        imprimirLista(s); print "}"
    return poblacioninicial

# Operador de cruce: crossover
def cruce(padre, madre, i1, i2):
    hijo = [0]*(nCiudades-1) # inicia el hijo con el mismo valor en todo el array
    if i1 < i2: i2 += 1     # normaliza: i1 siempre es menor que i2
    else: i1, i2 = i2, i1+1 # 
    hijo[i1:i2] = padre[i1:i2] # relleno el segmento en el hijo
    tam = nCiudades-(i2-i1)-1; # cuantos faltan para rellenar el hijo
    x=i2; y=i2
    for it in range(tam):
        if x == nCiudades-1: x=0 # empiezo desde el principio
        if y == nCiudades-1: y=0
        elem = madre[y]; y+=1
        if y == nCiudades-1: y=0
        while elem in hijo: # comprueba si esta ya en el hijo
            elem = madre[y]; y+=1;
            if y == nCiudades-1: y=0
        hijo[x] = elem; x+=1 # y lo introduce en el hijo
    return hijo

# mecanismo de reemplazo de una poblacion a otra
def reemplazo(vieja, intermedia):
    vieja = sorted(vieja, key=coste)
    intermedia = sorted(intermedia, key=coste)
    intermedia[nPoblacion-1] = vieja[1]
    intermedia[nPoblacion-2] = vieja[0]
    return intermedia

# cuerpo principal del algoritmo
def algoritmo():
    poblacionactual = obtenerpoblacioninicial()
    poblacionintermedia = []
    for i in range(1000): # numero de iteraciones
        poblacionintermedia = [] # resetea la pob intermedia
        print "\nITERACION:",i+1
        print "\nSELECCION"
        for ntorneo in range(nPoblacion): # TORNEO
            menor = 0;
            candidato1 = torneoAleatorio(); candidato2 = torneoAleatorio()
            coste1 = coste(poblacionactual[candidato1]); coste2 = coste(poblacionactual[candidato2])
            if coste1 <= coste2:
                menor = candidato1
            else:
                menor = candidato2
            print "\tTORNEO %i:" % ntorneo,candidato1,candidato2,"GANA",menor
            poblacionintermedia.append(list(poblacionactual[menor]))
        print "\nCRUCE"
        for ncruce in range(0,nPoblacion,2): # de 2 en 2
            aleatorio = floatAleatorio()
            print "\tCRUCE:",ncruce,ncruce+1,"(ALEATORIO: %.6f)"%aleatorio,
            if aleatorio>Pc:
                print "NO SE CRUZA"
            else:
                # CRUCE
                padre = poblacionintermedia[ncruce]
                madre = poblacionintermedia[ncruce+1]
                i1 = ciudadAleatoria()-1
                i2 = ciudadAleatoria()-1
                print "CORTES:",i1,i2
                hijo = cruce(padre, madre, i1, i2)
                hija = cruce(madre, padre, i1, i2)
                poblacionintermedia[ncruce] = list(hijo)
                poblacionintermedia[ncruce+1] = list(hija)
        print "\nMUTACION"
        for ind in range(nPoblacion):
            individuo = poblacionintermedia[ind]
            print "\tINDIVIDUO",ind
            for pos in range(len(individuo)):
                aleatorio = floatAleatorio()
                print "\t\tPOSICION:",pos,"(ALEATORIO %.6f) "%aleatorio,
                if aleatorio > Pm:
                    print "NO MUTA"
                else:
                    mutacion = ciudadAleatoria()-1
                    print "INTERCAMBIO CON:", mutacion
                    # MUTACION
                    poblacionintermedia[ind][mutacion],poblacionintermedia[ind][pos] = poblacionintermedia[ind][pos], poblacionintermedia[ind][mutacion]
        print "REEMPLAZO"
        poblacionactual = reemplazo(poblacionactual, poblacionintermedia)
        for ind in range(nPoblacion):
            individuo = poblacionactual[ind]
            print "INDIVIDUO",ind,"= {OBJETIVO: %i," % coste(individuo),"CAMINO:",
            imprimirLista(individuo); print "}"
leerDistancias()
leerAleatorios()
algoritmo()

