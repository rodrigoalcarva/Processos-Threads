import sys, pickle

#file = sys.argv[-1]
#comand = sys.argv[1]

def formateDate(microSeconds):
    """
    Recebe microsegundos e devolve horas, minutos, segundos e microsegundos
    """
    s = str(float(microSeconds)/1000000).split(".")
    
    m = 0
    h = 0

    if int(s[0]) >= 60:
        m += 1
        s[0] = "0"

    if m >= 60:
        h += 1
        m = 0

    return str(h) + ":" + str(m) + ":" + s[0] + ":" + s[1]


with open(file, "rb") as inFile:
    x = pickle.load(inFile)
    proc = []
    
    for el in x.keys():
        try:
            proc.append(int(el))
        except ValueError:
            pass
        
    #if command == '-b':
        #print os.getpid()
        #print ""
        #print ""

    #else:
        print "Inicio da execução da compressao/descompressao: " + x["data"]
            
        print "Duracao da execucao: " + formateDate(x["tempoDec"])

        sizeFile = []
        totalSize = 0

        for el in proc:
            
            nFiles = (len(x[el])-1)/3
            iFile = 1
            
            
            print "Processo: " + str(x[el][0])

            for i in range(nFiles):
                print "     Ficheiro processado: " + str(x[el][iFile])
                print "         tempo de compressão/descompressão: " + formateDate(x[el][iFile + 1])
                print "         dimensão do ficheiro depois de comprimido/descomprimido:  " + str(x[el][iFile + 2])
                sizeFile.append(x[el][iFile + 2])
                iFile += 3

            print "     Volume total de dados escritos em ficheiros: " + str(sum(sizeFile))
            totalSize += sum(sizeFile)

        print "Volume total de dados escritos em todos os ficheiros: " + str(totalSize)

