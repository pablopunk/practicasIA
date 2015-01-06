all:
	python ce.py > traza.txt && diff traza.txt traza_clase.txt > diferencia.txt
