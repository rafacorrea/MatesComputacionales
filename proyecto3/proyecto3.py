from graphviz import Digraph
import itertools

def parseFile(archivo):
    Q = []
    S = []
    F = []
    f = open(archivo, 'r')
    D = {}
    for line in f:
        linea = line.split()
        if linea[0] == 'q':
            Q.extend(linea[1:])
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
            tempDict = {key2 : values}
            if key not in D:
                D[key] = tempDict
            else:
                D[key].update(tempDict)            
   
    return Q, S, D, q, F

def calcQ(Q):
    Qf =[]
    for i in xrange(1,len(Q)+1):
        Qf.extend(list(itertools.combinations(Q,i)))
    result = [list(q) for q in Qf]
    return result

def calcF(Q, F):
    Ff =[]
    for f in F:
        Ff.extend([q for q in Q if f in q and q not in Ff])
    return Ff

def calcD(Q, D):
    D1 = {}
    for q in Q:
        for element in q:
            if repr(q) not in D1:
                D1[repr(q)] = D[element]
            else:
                A = D1[repr(q)]
                B = D[element]
                D1[repr(q)] = {x: list(set(A[x]).union(B[x])) for x in set(A).union(B)}

    print A                
    return D1
    
def calc(Q, S, D, q, F):
    Q1 = calcQ(Q)
    F1 = calcF(Q1, F)
    D1 = calcD(Q1, D)
    
def printAutomata():
    return 0
    
archivo = raw_input("Nombre del archivo?\n")        
Q, S, D, q, F = parseFile(archivo)
Q1 = calcQ(Q)
F1 = calcF(Q1, F)
D1 = calcD(Q1, D)
print D1

dot = Digraph(name='Automata', node_attr={'shape' : 'circle'})

for name in Q1:
    if name in F1:
        dot.node(repr(name), peripheries = '2')
    else:
        dot.node(repr(name))

quitar = '\other'
dot.node('INICIO', height = '0', fixedsize = 'true', label ='')


for key in D1:
    for i in D1[key]:
        destino = (D1[key][i])
        if len(destino) > 1 and quitar in destino :
            destino.remove(quitar)
        destino.sort()
        dot.edge(key, repr(destino), label=i)

  
dot.render('automata', view=True)
