#global
_strings = ['u', 'v', 'w', 'x', 'y', 'z']

#funcion que regresa dos listas: los strings base, y las reglas
def parseFile(archivo):
    f = open(archivo, 'r')
    base = f.readline().split()
    reglas = []
    for line in f:
        reglas = line.split()
    return base, reglas

#genera strings con n recursiones
def generarStrings(base, reglas, n):
    generados = base[:]
    viejos = generados[:]
    for x in xrange(n): #2
        for s in viejos:
            for regla in reglas:
                res = crearNuevo(s,regla, viejos)
                generados = list(set(generados).union(res))

        print 'iteracion %d: %s' % (x+1, list(set(generados) - set(viejos)))
        viejos = generados[:]

    
    generados.sort(key = lambda s: 0 if s == '\lambda' else len(s))
    return generados

#en base a la variable global strings, reemplaza lo necesario con el string que se le pasa
def crearNuevo(string, regla, viejos):
    generado = regla[:]
    temp = generado[:]
    res = []
    for s in _strings:
        generado = generado.replace(s, string)
        if len(generado) >= 2:
            generado = generado.replace('\lambda', '')
        if temp != generado:
            break
            
    if any(x in generado for x in _strings):
        for string in viejos:
            res.extend(crearNuevo(string, generado, viejos))
    else:
            if generado not in res:
                    res.append(generado)
    return res

#main
archivo = raw_input("Nombre del archivo?\n")
n = int(raw_input("Cuantos ciclos?\n"))
base, reglas = parseFile(archivo)
print "BASE: %s\nPASO RECURSIVO: %s\n" % ( ', '.join(str(x) for x in base), 
                                           ', '.join(str(x) for x in reglas) )
print "STRINGS GENERADOS EN %d CICLOS: %s" % (n, ', '.join(str(x) for x in generarStrings(base, reglas, n)))


