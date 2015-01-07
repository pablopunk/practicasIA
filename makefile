all:
	date; python ce.py > traza.txt; date && diff traza.txt traza_clase.txt > diferencia.txt
