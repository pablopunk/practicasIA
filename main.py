# Bibliotecas
import random
import itertools
import sys
import math

# Variables globales
n = 10  # Numero de ciudades
nIteraciones = 10  # numero de ejecuciones del algoritmo
distancias = {}  # diccionario para guardar las distancias entre las ciudades cargado del fichero
filein = "distancias_10.txt"
fileout = "ejecucion.txt"

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


# calcular la distancia total
def calcularDistancia(indices):
    i = 0;
    total = 0
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

    # todas las posibles permutaciones
    permutaciones = list(itertools.permutations(range(0, n - 1), 2))

    # Posiciones aleatorias
    random.shuffle(vecinoactual)

    while True:
        mejorvecino = vecinoactual[:]  # copio el vecino actual
        aux = []
        random.shuffle(permutaciones)  # orden aleatorio de las permutaciones

        # recorro todas las permutaciones posibles hasta que encuentre una distancia menor
        for i in range(len(permutaciones)):
            # prueba la permutacion
            aux = vecinoactual[:]
            intercambiar(aux, permutaciones[i][0], permutaciones[i][1])
            if calcularDistancia(aux) < calcularDistancia(mejorvecino):
                break

        if calcularDistancia(aux) < calcularDistancia(vecinoactual):
            vecinoactual = aux[:]

        if calcularDistancia(vecinoactual) >= calcularDistancia(mejorvecino):
            break

    return vecinoactual, calcularDistancia(vecinoactual)
    print "Distancia actual: %d" % calcularDistancia(vecinoactual)


# escribe los resultados del algoritmo varias veces en un fichero
def escribirFichero(iteraciones):
    media = 0;
    dist = list()  # voy a calcular la media y la desviacion
    menor = 1000000000;
    mayor = 0
    f = open(fileout, "w")
    for i in range(1, iteraciones + 1):
        solucion, distanciaTotal = algoritmo()
        media += distanciaTotal
        if distanciaTotal < menor:
            menor = distanciaTotal
        if distanciaTotal > mayor:
            mayor = distanciaTotal
        dist.append(distanciaTotal)
        f.write("Solucion %d:\t0 - " % i)
        for j in range(len(solucion)):
            f.write("%d - " % solucion[j])  # imprimo el array de indices
        f.write("0\tDistancia: %d KM\n" % distanciaTotal)

    # Media y desviacion
    media /= iteraciones
    desviacion = math.sqrt((sum([x * x for x in dist]) / iteraciones) - (media ** 2))
    f.write("\nMedia = %d\tDesviacion = %.2f" % (media, desviacion))
    f.write("\nMenor = %d\tMayor = %d\n" % (menor, mayor))
    f.close()
    print str(nIteraciones) + " guardadas en el fichero '" + fileout + "'"


def main():
    leerfichero()  # cargo los datos
    escribirFichero(nIteraciones)  # imprimo n iteraciones del algoritmo


if __name__ == '__main__':  # funcion main en el archivo main
    main()
