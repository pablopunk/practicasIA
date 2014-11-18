# Bibliotecas
import random 

# Variables globales
n=10 # Numero de ciudades
distancias={} # diccionario para guardar las distancias entre las ciudades cargado del fichero

# calcular la distancia total
def calcularDistancia(indices):
	i=0; total=0
	# sumo al total la distancia de 0 a 1
	aux = distancias[1]
	total += int(aux[0])
	# sumo al total la distancia de 0 a n-1
	aux = distancias[n-1]
	total += int(aux[0])

	for i in range(len(indices)-1):
		aux = indices[i]
		aux1 = indices[i+1]
		if aux1 < aux:
			array = distancias[aux]
			d = int(array[aux1])
		elif aux1 > aux:
			array = distancias[aux1]
			d = int(array[aux])
		# print "Distancia entre %d y %d: %d" % (aux,aux1,d)
		total += d
	return total

# lectura del fichero y carga de datos
def leerfichero():
	i=1; aux=[]
	f = open("distancias_10.txt","r")

	for linea in f.readlines():
		aux = linea.split()
		distancias[i] = aux
		i+=1

	# print distancias
	f.close()

# intercambiar dos posiciones aleatorias
def generar(lista):
	a=0; b=0
	otralista = lista[:]
	# dos indices aleatorios
	while a == b:
		a = random.randrange(0,n-1)
		b = random.randrange(0,n-1)
	# intercambio dos posiciones aleatorias
	aux = otralista[a]
	otralista[a] = otralista[b]
	otralista[b] = aux

	print otralista
	return otralista

# funcion principal
def main():

	leerfichero() # cargo los datos
	vecinoactual = range(1,n) # array de posiciones de las ciudades
	mejorvecino = []

	# Posiciones aleatorias
	random.shuffle(vecinoactual)
	print vecinoactual
	total = calcularDistancia(vecinoactual)
	print "Distancia total: %d" % total

	while True:

		mejorvecino = vecinoactual[:] # copio el vecino actual
		aux = []

		while True:
			aux = generar(vecinoactual)
			if calcularDistancia(aux) < calcularDistancia(mejorvecino):
				break

		if calcularDistancia(aux) < calcularDistancia(vecinoactual):
			vecinoactual = aux[:]

		print "Distancia actual: %d" % calcularDistancia(mejorvecino)

		if (calcularDistancia(vecinoactual) >= calcularDistancia(mejorvecino)):
			break

if __name__ == '__main__': # funcion main en el archivo main
	main()
