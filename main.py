import random
distancias={}
posiciones=[]
n=10

def imprimirDistancias(indices, diccionario):
	i=0
	for i in range(len(indices)-1):
		aux = indices[i]
		aux1 = indices[i+1]
		if aux1 < aux:
			array = diccionario[aux]
			d = int(array[aux1])
		elif aux1 > aux:
			array = diccionario[aux1]
			d = int(array[aux])
		print "Distancia entre %d y %d: %d" % (aux,aux1,d)

def leerfichero():
	i=1; aux=[]
	f = open("distancias_10.txt","r")

	for linea in f.readlines():
		aux = linea.split()
		distancias[i] = aux
		i+=1

	# print distancias
	f.close()

def main():
	posiciones = range(1,n)
	a=0; b=0

	while a == b:
		a = random.randrange(0,n-1)
		b = random.randrange(0,n-1)

	aux = posiciones[a]
	posiciones[a] = posiciones[b]	
	posiciones[b] = aux

	# solucionInicial = [a,b]
	print "Solucion inicial: intercambiar %d con %d" % (a,b)
	print posiciones
	imprimirDistancias(posiciones,distancias)

leerfichero()
main()