#colores ANSI
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE= '\033[4m'
    
#para agregar una linea del archivo o ingresada por el usuario al diccionario especificado   
def addToDict(line, gramatica):
    temp = line.strip().split('->')
    inicial = temp[0]
    final = temp[1]
    final = final.replace(" ", "")
    final = set(final.split('|'))
    if inicial not in gramatica:
        gramatica[inicial] = final
    else:
        gramatica[inicial] = gramatica[inicial].union(final)
    
#funcion que regresa la palabra a encontrar y un diccionario representando la gramatica
def parseFile(archivo):
    f = open(archivo, 'r')
    gramatica = {}
    inicio = f.readline().strip()
    inicio = inicio.replace(" ", "")
    string = f.readline().strip()
    string = string.replace(" ", "")
    for line in f:
        addToDict(line, gramatica)
            
            
    return string, gramatica, inicio

#donde se le pregunta todo al usuario
def menuPrincipal():
    choice = raw_input("Que desea hacer?\n1. Leer de un archivo\n2. Entrada a mano\n")
    choice = int(choice)
    if choice == 1:
        archivo = raw_input("Nombre del archivo?\n")
        string, gramatica, inicio = parseFile(archivo)
    if choice == 2:
        string, gramatica, inicio = entradaDatos()
    
    choice = int(raw_input("Que desea hacer?\n1. Derivar todo\n2. Derivar por la izquierda\n3. Derivar por la derecha\n0-EXIT\n"))
    while choice != 0:
        
        if choice == 1:
            n = int(raw_input("Numero de sustituciones?\n"))
            m = int(raw_input("Numero de derivaciones?\n"))
            res = derivarTodo('normal', gramatica, string, inicio, n, m)       
        if choice == 2:
            res = derivarTodo('izquierda', gramatica, string, inicio)
        if choice == 3:
            res = derivarTodo('derecha', gramatica, string, inicio)
            
        i = 0
        for elemento in res:
            i+=1
            print '\nderiviacion %i' % i
            print elemento
        choice = int(raw_input("Que desea hacer?\n1. Derivar todo\n2. Derivar por la izquierda\n3. Derivar por la derecha\n0-EXIT\n"))
#entrada manual
def entradaDatos():
    gramatica = {}
    
    string = raw_input("Ingrese el string a revisar\n")
    string = string.replace(" ","")
    
    line = raw_input("Ingrese la gramatica, con formato A->B\n")
    while line != '0':
        addToDict(line, gramatica)
        line = raw_input("Ingrese otra regla, 0 para terminar\n")
    inicio = raw_input("Ingrese el simbolo inicial (usualmente S)")
    return inicio, string, gramatica

#opcion 1, derivar todo
def derivarTodo(tipo, gramatica, string, inicio = 'S', n = 100, m = 100):
    resultado = []
    derivaciones = 0
    sustituciones = 0
    #generado = 'S'
    generado = inicio
    viejos = []
    nuevos = [generado]
    reemplazadosV = []
    reemplazados = ['']
    
    for i in xrange(n):
        viejos = nuevos[:]
        nuevos = []
        reemplazadosV = reemplazados[:]
        reemplazados =[]
        #para el indice de la palabra
        idGenerado = 0
        #para cada P generado...
        for generado in viejos:
            #para el indice del caracter
            idChar = ((len(generado) - 1) if tipo == 'derecha' else 0)
            for char in (reversed(generado) if tipo == 'derecha' else generado ):
                #si es una variable (mayuscula)
                #if char in vars:
                if char.isupper():
                    #para cada regla gramatica..
                    for rep in gramatica[char]:                     
                        temp = generado[:idChar] + bcolors.FAIL + generado[idChar] + bcolors.ENDC + generado[idChar+1:]
                        #generar string representando el camino
                        camino = reemplazadosV[idGenerado] + temp + ' (' + char + '->' + rep + ')|'
                        #agregar al arreglo que corresponde con los nuevos elementos generados
                        reemplazados.append(camino)
                        #reemplazar lambda/espacios en blanco
                        if rep == "_":
                            rep = ""
                        temp = generado[:idChar] + rep + generado[idChar+1:]
                        #si es terminal (minusculas) y es igual al string de entrada...
                        if temp == string and temp.islower():  
                            camino += string  
                            resultado.append(camino)
                            derivaciones+=1
                            
                            if tipo == 'izquierda' or tipo == 'derecha':
                                return resultado
                            #revisar si se llego al limite de derivaciones
                            if derivaciones >= m:
                                return resultado
                        nuevos.append(temp)
                    if tipo == 'izquierda' or tipo == 'derecha':
                        break
                idChar = (idChar - 1 if tipo == 'derecha' else idChar + 1)         
            idGenerado+=1
    return resultado

#main
menuPrincipal()
