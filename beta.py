import os
import time
import datetime
import getpass
import numpy as np
start_time = time.time()

#Jesteśmy w katalogu testsuite
#Funkcja liczy linie z nazwami folderów testów
def count():
    testList = list(np.genfromtxt("tlist.txt", dtype=str, comments="#"))
    return testList, len(testList)

#Funkcja sprawdza czy dany test istnieje
def testIsPresent(testName, ii):
    if os.path.exists(testName):
        listOfFolders.append('{}'.format(testName))
        listOfTags.append('test{}'.format(ii))
        return True
    else:
        listOfFolders.append('Test {} does not exist'.format(testName))
        listOfTags.append('FAIL of test-{}'.format(ii))
        listOfMakes.append('FAIL')
        listOfRuns.append('FAIL')
        listOfChecks.append('FAIL')
        return False

#Funkcja sprawdza czy  w danym teście istnieje plik test_desc
def testDescIsPresent(nameOfFolder, folderIsPresent):
    if folderIsPresent:
        os.chdir('C:/Users/maxio/Desktop/Pythong/{}'.format(nameOfFolder)) # Jeżeli folder istnieje to wchodzi do niego
        if os.path.exists('test_desc.txt'): return True # Jeżeli test.desc istnieje to zwraca True
        else: # Jeżeli test.desc nie istnieje to dodaje FAIL dla makes/run/checks
            listOfMakes.append('FAIL')
            listOfRuns.append('FAIL')
            listOfChecks.append('FAIL')
            return False
    else: return False

#Funkcja wywołująca komendy z pliku test_desc
def runLinuxCommands(nowpath):
    file = open('test_desc.txt', "r").read().split('\n')  # otwiera plik i czyta linia po linii bez enterów
    line_count = 0  # licznik linii
    for line in file:  # pętla wykonuje się tak długo aż plik ma linie
        tag, command = line.split(": ")  # tworzy 2 stringi nadpisywane co iteracje
        print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command)  # outputuje komendę dla danej linii pliku
        if line != "\n": # Jeżeli linia NIE JEST Enterem to licznik++
            line_count += 1
        if tag == 'tag': continue # Pomija ten tag i idzie do następnego kroku w pętli, czyli do następnej linii pliku
        if tag == 'exec':  # wykonanie komendy
            os.system(command)
        if tag == 'test':  # sprawdzenie czy pliki istnieją
            file_list = os.listdir(nowpath)
            possible_files = [fn for fn in file_list if '-wslda-' in fn]
            if not possible_files: now_make = 'FAIL'
            else: now_make = 'OK'
            if os.path.exists('test1_cmp.txt'): now_run = 'OK'
            else: now_run = 'FAIL'
        if tag == 'diff': pass
    return now_make, now_run

#Funkcja porównująca wartości outputowe cmp z referencyjnymi ref
def runDiffTest():
    valsCmp, valsRef, valsTol, comparedValues = [], [], [], []
    with open('test1_cmp.txt') as f1:
        next(f1)
        for line1 in f1:
            cmp_tag, cmp_value = line1.split()
            valsCmp.append(float(cmp_value.rstrip('\n')))
    with open('test1_ref.txt') as f2:
        next(f2)
        for line2 in f2:
            ref_tag, ref_value, ref_tolerance = line2.split()
            valsRef.append(float(ref_value.rstrip('\n')))
            valsTol.append(float(ref_tolerance.rstrip('\n')))
    for i in range(len(valsCmp)):
        if abs(valsCmp[i] - valsRef[i]) < valsTol[i]:
            comparedValues.append('OK')
        else: comparedValues.append('FALSE')
    if all(values == 'OK' for values in comparedValues): now_check = 'OK'
    else: now_check = 'FALSE'
    return now_check

#Funkcja generująca raport
def runReport(Lfolder, Ltag, Lmake, Lrun, Lcheck):
    nameReport = getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")
    filepath = 'C:/Users/maxio/Desktop/Pythong/' + nameReport + '.txt'
    f = open(filepath, 'w')
    f.write('Folder\tTag\tMake\tRun\tCheck\n')
    for ii in range(len(Lfolder)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(Lfolder[ii], Ltag[ii], Lmake[ii], Lrun[ii], Lcheck[ii]))
    f.close()

#Main
os.chdir('C:/Users/maxio/Desktop/Pythong') #Ustawiamy się w folderze roboczym /home2/scratch/knfk/cold-atoms/testsuite
listOfTests, N = count() # Zapis do listy nazwy testów i ile ich ma być do wykonania
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks, listOfErrors = [], [], [], [], [], []
for i in range(1, N+1):
    nameOfTest = listOfTests[i-1]
    ifdir = testIsPresent(nameOfTest, i) #Sprawdza czy dany folder z wypisanych w liście istnieje: zwraca T/F
    ifdesc = testDescIsPresent(nameOfTest, ifdir) #Sprawdza czy w danym folderze, który istnieje jest plik test.desc: zwraca T/F
    #Oba powyższe muszą być ustawione na True, inaczej pętla przejdzie do następnego folderu z testem.
    if ifdir and ifdesc:
        os.chdir('C:/Users/maxio/Desktop/Pythong/{}'.format(nameOfTest))
        make, run = runLinuxCommands(os.getcwd())
        listOfMakes.append(make)
        listOfRuns.append(run)
        check = runDiffTest()
        listOfChecks.append(check)
    else: continue

print(listOfFolders, len(listOfFolders))
print(listOfTags, len(listOfTags))
print(listOfMakes, len(listOfMakes))
print(listOfRuns, len(listOfRuns))
print(listOfChecks, len(listOfChecks))

runReport(listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks)
print('Done.')
print("--- %.8s seconds ---" % (time.time() - start_time))
