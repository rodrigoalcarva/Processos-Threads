import sys, os, zipfile
from threading import Thread
from multiprocessing import Semaphore

args = sys.argv[1:]
comand = []
files = []

for el in args:
    if "-" in el:
        comand.append(el)
    elif prev == '-p':
        #Verifica se numero de threads é um inteiro
        try:
            nT = int(el)
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
    global ind
    global noFile
    global f

    #Semaforo usado para garantir que multiplos processos não acedem ao ind em simultâneo
    mutex.acquire()
    
    while ind < len(files) and noFile == 1: 
        
        zname = files[ind]
        ind += 1
        
        if os.path.isfile(zname):
                f += 1
                mutex.release()
                c = True

        else:        
            print 'Ficheiro ' + zname + ' nao existe'
            if '-t' in comand:
                noFile = 0
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

    if  ind == len(files) or noFile == 0:
        mutex.release()


mutex = Semaphore(1)
ind = 0
noFile = 1
f = 0


#Cria n threads
if "-p" in comand:
    t = []

    for i in range(nT):
        newT = Thread(target = com_des)
        t.append(newT)
        
    for th in t:
        th.start()
        
    for th in t:
        th.join() 

    
else:
    com_des()


print "Numero de ficheiros comprimidos/descomprimidos: ", f
