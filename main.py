# Bibliotecas
import random 

# Variables globales
n=10 # Numero de ciudades
distancias={} # diccionario para guardar las distancias entre las ciudades cargado del fichero

# imprime las distancias (del diccionario) entre las ciudades cuyos indices estan juntos en el array 'indices'
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

# funcion principal
def main():

	leerfichero() # cargo los datos
	posiciones = range(1,n) # array de posiciones de las ciudades
	a=0; b=0 # indices a cambiar 

	while a == b: # son aleatorios pero no pueden ser el mismo (porque no se cambiarian)
		a = random.randrange(0,n-1)
		b = random.randrange(0,n-1)

	# intercambio los indices a y b
	aux = posiciones[a]
	posiciones[a] = posiciones[b]	
	posiciones[b] = aux

	# solucionInicial = [a,b]
	print "Solucion inicial: intercambiar %d con %d" % (a,b)
	print posiciones
	imprimirDistancias(posiciones,distancias)

if __name__ == '__main__': # funcion main en el archivo main
	main()