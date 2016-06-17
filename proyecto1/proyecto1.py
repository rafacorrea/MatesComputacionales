#funcion que regresa dos listas: una es el set de los elementos, la otra una lista de tuplas con las relaciones
def parseFile(archivo):
    f = open(archivo, 'r')
    cuantos = int(f.readline())
    set1 = []
    relaciones = []
    for line in f:
        par = line.split()
        relaciones.append(par)    
        if par[0] not in set1:
            set1.append(par[0])
        if par[1] not in set1:
            set1.append(par[1])
    return set1, relaciones

#funcion que al recibir las listas del set y de las relaciones, determina si se es reflexiva
def testReflexiva(set1, relaciones):
    for elemento in set1:
        test = [elemento, elemento]
        if test not in relaciones:
            return False
    return True

#funcion que al recibir las listas del set y de las relaciones, determina si se es irreflexiva
def testIrreflexiva(set1, relaciones):
    for elemento in set1:
        test = [elemento, elemento]
        if test in relaciones:
            return False
    return True 

#funcion que al recibir las listas del set y de las relaciones, determina si se es transitiva
def testTransitiva(set1, relaciones):
    for relacion in relaciones:
        a = relacion[0]
        b = relacion[1]
        for busqueda in relaciones:
            if busqueda[0] == b:
                c = busqueda[1]
                if([a,c] not in relaciones):
                    return False       
    return True

#funcion que al recibir las listas del set y de las relaciones, determina si se es simetrica
def testSimetria(set1, relaciones):
    for relacion in relaciones:
        a = relacion[0]
        b = relacion[1]
        if([b,a] not in relaciones):
            return False       
    return True

#funcion que al recibir las listas del set y de las relaciones, determina si se es asimetrica
def testAsimetria(set1, relaciones):
    for relacion in relaciones:
        a = relacion[0]
        b = relacion[1]
        if([b,a] in relaciones):
            return False       
    return True

#funcion que al recibir las listas del set determina las relaciones con las que se cumple
def testAll(set1, relaciones):
    respuesta = []
    if(testReflexiva(set1, relaciones)):
        respuesta.append('REFLEXIVA')
    if(testIrreflexiva(set1, relaciones)):
        respuesta.append('IRREFLEXIVA')
    if(testTransitiva(set1, relaciones)):
        respuesta.append('TRANSITIVA')
    if(testSimetria(set1, relaciones)):
        respuesta.append('SIMETRICA')
    if(testAsimetria(set1, relaciones)):
        respuesta.append('ASIMETRICA')
    
    if not len(respuesta):
        respuesta.append('NO CUMPLE NINGUNA')
        
    return respuesta
    
#preguntar el nombre del archivo
archivo = raw_input("Nombre del archivo?\n")

#llamar la funcion con el nombre del archivo
set1, relaciones = parseFile(archivo)

#resultados
print 'El conjunto S es: %s' % set1 
print 'Las relaciones son: %s' % testAll(set1, relaciones)

