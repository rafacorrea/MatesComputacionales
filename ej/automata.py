finales = [0]
alfabeto = ['0', '1']
automata = [[1, 2], [0, 3], [3, 0], [2, 1]]

string1 = raw_input("string?")
actual = 0
for c in string1:
    indice = alfabeto.index(c)
    actual = automata[actual][indice]

if actual in finales:
    print "ACEPTADO\n"
else:
    print "RECHAZADO\n'"
