import os
import time
import numpy as np
start_time = time.time()

def amountOfDirs(): # funkcja zliczająca foldery
    os.chdir('/home/prohackerxxx/Desktop/testsuitePython/knfk')
    workPath = os.getcwd()
    return int(len(next(os.walk(workPath))[1]) / 2)

#Jesteśmy w katalogu testsuite
#Funkcja liczy linie z nazwami folderów testów
def count():
	testList = np.genfromtxt("tlist.txt", dtype=str)
	return testList, len(testList)
listOfTests, N = count()

#Funkcja sprawdza czy dany test istnieje
def ifTestExists(testName):
    if os.path.exists(testName):
        return True
    else:
        listOfMakes.append('FAIL at {}'.format(testName))
        listOfRuns.append('FAIL'.format(testName))
        listOfChecks.append('FAIL'.format(testName))
        return False

#Funkcja wywołująca komendy z pliku test_desc
def runLinuxCommands(nowpath):
    file = open('test_desc.txt', "r").read().split('\n')  # otwiera plik i czyta linia po linii bez enterów
    line_count = 0  # licznik linii
    for ii in file:  # pętla wykonuje się tak długo aż plik ma linie
        tag, command = ii.split(": ")  # tworzy 2 stringi nadpisywane co iteracje
        print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command)  # outputuje komendę dla danej linii pliku
        if ii != "\n": # Jeżeli linia NIE JEST Enterem to licznik++
            line_count += 1
        if tag == 'tag': continue # Pomija ten tag i idzie do następnego kroku w pętli, czyli do następnej linii pliku
        if tag == 'exec':  # wykonanie komendy
            os.system(command)
        if tag == 'test':  # sprawdzenie czy pliki istnieją
            file_list = os.listdir(nowpath)
            possible_files = [fn for fn in file_list if '-wslda-' in fn]
            if not possible_files: now_make = 'FAIL'
            else: now_make = 'OK'
            del possible_files, file_list
            if os.path.exists('test1_cmp.txt'): now_run = 'OK'
            else: now_run = 'FAIL'
        if tag == 'diff': continue
    return now_make, now_run

#Funkcja porównująca wartości outputowe cmp z referencyjnymi ref
def runDiffTest():
    listOfValues = []
    with open('test1_cmp.txt') as bf1:
        with open('test1_ref.txt') as bf2:
            for line1, line2 in zip(bf1, bf2):
                cmp_tag, cmp_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z outputu
                ref_tag, ref_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z referencyjnego
                listOfValues.append(float(cmp_value.rstrip('\n')) - float(ref_value.rstrip('\n')))
    if all(comparedValue < 10e-3 for comparedValue in listOfValues): now_check = 'OK'
    else: now_check = 'FALSE'
    return now_check

#Funkcja generująca raport
def report(folder, tag, make, run, check):
    filepath = '/home/prohackerxxx/Desktop/testsuitePython/knfk/NowyOutput.txt' #home2/archive/....
    if os.path.isfile(filepath):
        os.remove(filepath)
    f = open(filepath, 'w')
    f.write('Folder\tTag\tMake\tRun\tCheck\n')
    for ii in range(len(folder)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(folder[ii], tag[ii], make[ii], run[ii], check[ii]))
    f.close()

#Main
N = amountOfDirs()
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks = [], [], [], [], []
for i in range(1, N+1):
    if not ifTestExists(i): pass
    else:
        path = '/home/prohackerxxx/Desktop/testsuitePython/knfk/st-test-{}'.format(i)
        os.chdir(path) #Wchodzimy do folderu st-test-i
        make, run = runLinuxCommands(path)
        listOfMakes.append(make)
        listOfRuns.append(run)
        del make, run
        check = runDiffTest()
        listOfChecks.append(check)
        del check

report(listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks)
print('Done.')
print("--- %.8s seconds ---" % (time.time() - start_time))
