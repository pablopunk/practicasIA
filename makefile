all:
	date # fecha de inicio
	pypy tabu.pyc || ( echo "No se encuentra pypy en el sistema (recomendado para mejorar la eficiencia), se usará python" && python taby.p )
	date # fecha de fin
