from graphviz import Digraph
import itertools

#Parsear el archivo
def parseFile(archivo):
    empty = '\empty'
    Q = set([])
    S = []
    F = []
    f = open(archivo, 'r')
    D = {}
    for line in f:
        linea = line.split()
        if linea[0] == 'q':
            Q.update(linea[1:])
        if linea[0] == 'e':
            S.extend(linea[1:])
        if linea[0] == 'i':
            q =linea[1]
        if linea[0] == 'f':
            F.extend(linea[1:])
        if linea[0] == 'd':
            key = linea[1]
            key2 = linea[2]
            values = linea[3:]
            if empty in values:
                values.remove(empty)
            tempDict = {key2 : set(values)}
            if key not in D:
                D[key] = tempDict
            else:
                D[key].update(tempDict)            
      
    #para rellenar, si esta incompleta la tabla
    for estado in Q:
        if estado not in D:
            for entrada in S:
                tempDict = {entrada : []}
                D[estado] = tempDict
        else:
            for entrada in S:
                if entrada not in D[estado]:
                    D[estado][entrada]=[]

    Q = sorted(Q)            
    return Q, S, D, q, F

#calcular Q'
def calcQ(Q):
    Qf =[]
    for i in xrange(1,len(Q)+1):
        Qf.extend(list(itertools.combinations(Q,i)))
    result = [list(q) for q in Qf]
    return result

#calcular F'
def calcF(Q, F):
    Ff =[]
    for f in F:
        Ff.extend([q for q in Q if f in q and q not in Ff])
    return Ff

#calcular delta'
def calcD(Q, D):
    D1 = {}
    for q in Q:
        for element in q:
            if element in D:
                if repr(q) not in D1:
                    D1[repr(q)] = D[element]
                else:
                    A = D1[repr(q)]
                    B = D[element]
                    D1[repr(q)] = {x: list(set(A[x]).union(B[x])) for x in set(A).union(B) if x in A and x in B}

    return D1

#calcular todo  
def calc(Q, S, D, q, F):
    Q1 = calcQ(Q)
    F1 = calcF(Q1, F)
    D1 = calcD(Q1, D)
    print("\nCreando Automatas...\n")
    printAutomata(Q1, D1, F1, q)
    printSimple(D1,F1, q)
    print("Escribiendo resultado...\n")
    escribirResultados(Q1, S, D1, q, F1)
     
def printAutomata(Q,D,F,q):
    dot = Digraph(name='Automata', node_attr={'shape' : 'circle'})

    for name in Q:
        if name in F:
            dot.node(repr(name), peripheries = '2')
        else:
            dot.node(repr(name))
    
    #
    dot.node('INICIO', height = '0', fixedsize = 'true', label ='')
    dot.edge('INICIO', repr([q])) 
    
    for key in D:
        for i in D[key]:
            destino = (D[key][i])
            #sort para que los subconjuntos siempre esten en el mismo orden
            destino = sorted(destino)
            if len(destino):
                dot.edge(key, repr(destino), label=i)
            #ELSE: emtpy
      
    dot.render('automataCompleto', view=True)
    return 0


def printSimple(D, F, q):
    dot = Digraph(name='Automata', node_attr={'shape' : 'circle'})
    #nodo dummy
    dot.node('INICIO', height = '0', fixedsize = 'true', label ='')
    dot.edge('INICIO', repr([q]))
    
    recorrido = []
    recorrer(D, F, [q], dot, recorrido )
    dot.render('automataSimple', view=True)

def recorrer(D,F,q,dot, recorrido):
    recorrido.append(repr(q))
    key = repr(q)
    for i in D[key]:
        destino = (D[key][i])
        #sort para que los subconjuntos siempre esten en el mismo orden
        destino = sorted(destino)
        if q in F:
            dot.node(key, peripheries = '2')
            
        if len(destino):
            dot.edge(key, repr(destino), label = i)
        
            #Busca si ya recorrio este nodo...
            if repr(destino) not in recorrido:
                #recorre para los destinos
                recorrer(D, F, destino, dot, recorrido)

def escribirResultados(Q, S, D, q, F):
        f = open('resultado', 'w+')
        myList = []
        for elemento in Q:
            myList.append(repr(elemento))
        myString = " ".join( myList )
        f.write('q %s\n' % myString)
        myString = " ".join( S )
        f.write('e %s\n' % myString)
        for key in D:
            for i in D[key]:
                destino = repr(list(D[key][i]))
                f.write('d %s %s %s\n' % (key, i, destino))
        f.write('i %s\n' % [q])
        myList =[]
        for elemento in F:
            myList.append(repr(elemento))
        myString = " ".join( myList )
        f.write('f %s\n' % myString)
        
archivo = raw_input("Nombre del archivo?\n")     
calc(*parseFile(archivo))
print("Resultados en el archivo 'resultado'\nAutomatas en formato PDF 'automataCompleto.pdf' y 'automataSimple.pdf'")
