import sys, os, zipfile, signal, time, pickle
from multiprocessing import Process, Value, Semaphore, Queue
from datetime import datetime

args = sys.argv[1:]
comand = []
files = []

#Inicia construcao de dicionario de info
date =  datetime.now().strftime("%d/%B/%Y, %H:%M:%S:%f")
infDict = {"data": date}

t1 = time.time()


for el in args:
    if "-" in el:
        comand.append(el)
    elif prev == '-p':
        #Verifica se numero de processos e um inteiro
        try:
            nP = int(el)
        except ValueError:
            raise ValueError("Numero de processos nao e inteiro")
    elif prev == '-a':
        try:
            nA = int(el)
        except ValueError:
            raise ValueError("Intervalo de tempo nao valido")
    elif prev == '-f':
        try:
            fName = el
        except IOError:
            raise IOError("Ficheiro nao encontrado")
    else:
        files.append(el)
    prev = el
        
if len(files) == 0:
    files = sys.stdin.readline().split(" ")


def sTrue(sig, Null):
    """
    Handler do SIGINT
    """
    s.value = 0

    
def estado(sig, Null):
    """
    Handler do Alarm signal
    """
    zipFiles = [s + ".zip" for s in files]
    
    print "Numero de ficheiros comprimidos/descomprimidos: ", f.value
    sizeAlarm = []
    
    for i in range(f.value):
        sizeAlarm.append(float(os.path.getsize(zipFiles[i]))/1024)

    t3 = time.time()
    print "Volume de dados escritos: " + str(sum(sizeAlarm))
    print "Tempo decorrido: ",str((t3 - t1)*1000000)
    #print "Não comprimidos/descomprimidos: " + str(len(zipFiles) - f.value)
    #print 


#Mudanca do handler do SIGINT
signal.signal(signal.SIGINT, sTrue)

#Verifica para mudanca do handler de alarm
if '-a' in comand:
    signal.signal(signal.SIGALRM, estado)
    signal.alarm(nA)    

        
def com_des():
    """
    Faz a compressao ou descompressao dos ficheiros
    Dependendo a opcao '-c' ou '-d' respetivamente
    """    
    #Semaforo usado para garantir que multiplos processos nao acedem ao ind em simultaneo
    mutex.acquire()
    
    ##t8 = time.time()

    p = [os.getpid()]
        
    while ind.value < len(files) and noFile.value == 1 and s.value == 1:

        t4 = time.time()        
        zname = files[ind.value]        
        ind.value += 1
        
        if os.path.isfile(zname):
            f.value += 1
            mutex.release()
            c = True
            
        ficheiro = 0

        else:        
            print 'Ficheiro ' + zname + ' nao existe'
            if '-t' in comand:
                noFile.value = 0
            mutex.release()
            c = False

        if c:
            if comand[0] == '-c':
                zname = zname + '.zip'
                with zipfile.ZipFile(zname, mode='w') as zfile:
                    zfile.write(zname[:-4])
                    
                    
            elif comand[0] == '-d':
                znameD = zname[:-4]
                with zipfile.ZipFile(zname, mode='r') as zfile:
                    zfile.extract(znameD)
                    
            t5 = time.time()

            p.append(zname)
            p.append((t5 - t4)*1000000)
            p.append(os.path.getsize(zname))
    
    if  ind.value == len(files) or noFile.value == 0 or s.value == 0:
        q.put(p)
        mutex.release()
        #t9 = time.time()
        #if '-x' in comand:
           #print ((t9 - t8) * 1000000)


mutex = Semaphore(1)
ind = Value("i", 0)
noFile = Value("i", 1)
f = Value("i", 0)
s = Value("i", 1)
q = Queue()

#Cria n processos
if "-p" in comand:
    p = []

    for i in range(nP):
        newP = Process(target = com_des)
        p.append(newP)
    
    for proc in p:
        proc.start()
        
    for proc in p:
        proc.join() 
    
else:
    nP = 1
    com_des()
    

t2 = time.time()
endFiles = []

for i in range(nP):
    el = q.get()
    if len(el) > 3:
        infDict[i] = el
        n = 1
        for ind in range(len(el)/3):
            endFiles.append(el[n])
            n += 3
    elif len(el) > 1 and len(el) <= 3:
        infDict[i] = el
        endFiles.append(el[1])

infDict["tempoDec"] = (str((t2 - t1)*1000000))

if '-f' in comand:
    with open(fName, "wb") as outFile:
        pickle.dump(infDict, outFile, 1)

size = []

for i in range(len(endFiles)):
    size.append(float(os.path.getsize(endFiles[i]))/1024)

print "Numero de ficheiros comprimidos/descomprimidos: ", f.value

if s.value == 0:
    print "Volume de dados escritos: " + str(sum(size))
    print "Tempo decorrido: ",str((t2 - t1)*1000000)
