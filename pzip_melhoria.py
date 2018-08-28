import sys, os, zipfile
from multiprocessing import Process, Value, Semaphore

args = sys.argv[1:]
comand = []
files = []

for el in args:
    if "-" in el:
        comand.append(el)
    elif prev == '-p':
        #Verifica se numero de processos é um inteiro
        try:
            nP = int(el)
        except ValueError:
            raise ValueError("Numero de processos nao e inteiro")
    else:
        files.append(el)
    prev = el


if len(files) == 0:
    files = sys.stdin.readline().split(" ")
        
    
def com_des():
    """
    Faz a compressão ou descompressão dos ficheiros
    Dependendo a opção '-c' ou '-d' respetivamente
    """
    #Semaforo usado para garantir que multiplos processos não acedem ao ind em simultâneo
    mutex.acquire()
    
    while ind.value < len(files) and noFile.value == 1: 
        
        zname = files[ind.value]
        ind.value += 1
        
        if os.path.isfile(zname):
                f.value += 1
                mutex.release()
                c = True

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

    if  ind.value == len(files) or noFile.value == 0:
        mutex.release()


mutex = Semaphore(1)
ind = Value("i", 0)
noFile = Value("i", 1)
f = Value("i", 0)


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
    com_des()


print "Numero de ficheiros comprimidos/descomprimidos: ", f.value 


