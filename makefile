all:
	date # fecha de inicio
	pypy tabu.py || ( echo "No se encuentra pypy en el sistema (recomendado para mejorar la eficiencia), se usara python" && python tabu.py )
	date # fecha de fin
