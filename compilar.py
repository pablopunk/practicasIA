import sys
import py_compile

if len(sys.argv) < 1:
	print "Usage: python compilar.py path/to/file.py"
else:
	py_compile.compile(sys.argv[1])