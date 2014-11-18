# Bibliotecas
import random 
import itertools

# Variables globales
n=10 # Numero de ciudades
distancias={} # diccionario para guardar las distancias entre las ciudades cargado del fichero

# calcular la distancia total
def calcularDistancia(indices):
	i=0; total=0
	# sumo al total la distancia de 0 a 1
	aux = distancias[indices[0]]
	total += int(aux[0])
	# sumo al total la distancia de 0 a n-1
	aux = distancias[indices[n-2]]
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

def intercambiar(lista, a, b):
	aux = lista[a]
	lista[a] = lista[b]
	lista [b] = aux

# funcion principal del algoritmo
def algoritmo():
	vecinoactual = range(1,n) # array de posiciones de las ciudades
	mejorvecino = []

	# Posiciones aleatorias
	random.shuffle(vecinoactual)

	while True:

		mejorvecino = vecinoactual[:] # copio el vecino actual
		aux = []

		# todas las posibles permutaciones
		permutaciones = list(itertools.permutations(range(0,n-1), 2))

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

	print vecinoactual
	print "Distancia actual: %d" % calcularDistancia(vecinoactual)

def main():
	leerfichero() # cargo los datos
	algoritmo()

if __name__ == '__main__': # funcion main en el archivo main
	main()
