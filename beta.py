import datetime
import getpass
import logging
import numpy as np
import os
import time

#konfiguracja loggera w konsoli
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#konfiguracja loggera w pliku testsuite.log
#logging.basicConfig(filename='testsuite.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#wyłączenie wszystkich komunikatów loggera
#logging.disable(logging.CRITICAL)
logging.debug("Uruchomienie modulu testsuite.")
start_time = time.time()

#Funkcja ustawia domyślny folder roboczy dla całego procesu testowania /home2/scratch/knfk/cold-atoms/testsuite
def setwd():
	return '/home/prohackerxxx/Desktop/testsuitePython/knfk'
	# return 'C:/Users/maxio/Desktop/Pythong'

#Jesteśmy w katalogu testsuite
#Funkcja liczy linie z nazwami folderów testów
def count():
	logging.info("Liczenie testów.")
	testList = list(np.genfromtxt("tlist.txt", dtype=str, comments="#"))
	return testList, len(testList)

#Funkcja sprawdza czy dany test istnieje
def testIsPresent(testName):
	logging.info("Sprawdzanie czy test\"" + testName + "\" istnieje.")
	if os.path.exists(testName):
		listOfFolders.append('{}'.format(testName))
		logging.info("Znaleziono test \"" + testName + "\".")
		return True
	else:
		listOfFolders.append(testName)
		listOfTags.append('FAIL')
		listOfMakes.append('FAIL')
		listOfRuns.append('FAIL')
		listOfChecks.append('FAIL')

		logging.info("Test \"" + testName + "\" nie istnieje.")

	return False

#Funkcja sprawdza czy  w danym teście istnieje plik test_desc
def testDescIsPresent(nameOfFolder, folderIsPresent):
	if folderIsPresent:
		os.chdir(setwd()+'/{}'.format(nameOfFolder)) # Jeżeli folder istnieje to wchodzi do niego		
		logging.debug("Otwarto folder \"" + str(setwd()+'/{}'.format(nameOfFolder)) + "\".")

		if os.path.exists('test.desc'):
			listOfTags.append('OK')
			logging.info("Znaleziono plik \"test.desc\" w folderze \"" + nameOfFolder + "\".")
			return True # Jeżeli test.desc istnieje to zwraca True
		else: # Jeżeli test.desc nie istnieje to dodaje FAIL dla makes/run/checks
			listOfTags.append('FAIL')
			listOfMakes.append('FAIL')
			listOfRuns.append('FAIL')
			listOfChecks.append('FAIL')

			logging.info("\"test.desc\" nie istnieje w folderze \"" + nameOfFolder + "\".")

			return False
	else:
		logging.info("Folder \"" + nameOfFolder + "\" nie istnieje.") 
		return False

#Funkcja sprawdza czy w danym katalogu istnieje plik referencyjny .ref
def refFile(nowpath):
	logging.info("Sprawdzanie obecności plików referencyjnych .ref.")
	file_list = os.listdir(nowpath)
	possible_files = [fn for fn in file_list if 'ref' in fn]
	if possible_files == []:
		logging.info("Nie znaleziono pliku .ref.")		
		return False
	
	else: return True

#Funkcja wywołująca komendy z pliku test_desc
def runLinuxCommands(nowpath):
	logging.info("Wykonywanie komend z pliku \"test.desc\".")
	file = open('test.desc', "r").read().split("\n")  # otwiera plik i czyta linia po linii bez enterów
	line_count = 0  # licznik linii
	for line in file:  # pętla wykonuje się tak długo aż plik ma linie		
		if len(line) == 0: continue
		else: pass
		tag, command = line.split(": ")  # tworzy 2 stringi nadpisywane co iteracje
		print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command)  # outputuje komendę dla danej linii pliku
		if tag == 'tag': continue # Pomija ten tag i idzie do następnego kroku w pętli, czyli do następnej linii pliku
		if tag == 'exec':  # wykonanie komendy
			os.system(command)
		if tag == 'test':  # sprawdzenie czy pliki istnieją
			file_list = os.listdir(nowpath)
			possible_files = [fn for fn in file_list if '-wslda-' in fn]
			if not possible_files: 
				now_make = 'FAIL'
				logging.info("Nie odnaleziono plikow \"-wslda-\".")
			else: now_make = 'OK'
			if os.path.exists('test1_cmp.txt'): now_run = 'OK'
			else: 
				now_run = 'FAIL'
				logging.info("Plik \"test1_cmp.txt\" nie istnieje.") 
		if tag == 'diff': pass

		line_count += 1

	return now_make, now_run

#Funkcja porównująca wartości outputowe cmp z referencyjnymi ref
def runDiffTest():
	logging.info("Sprawdzanie wartości referencyjnych.")
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
		else: comparedValues.append('FAIL')
	if all(values == 'OK' for values in comparedValues): now_check = 'OK'
	else: now_check = 'FAIL'
	return now_check

#Funkcja generująca raport
def runReport(Lfolder, Ltag, Lmake, Lrun, Lcheck):
	logging.info("Generowanie raportu.")
	filepath = setwd() + getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M") + '.txt'
	f = open(filepath, 'w')
	f.write('Folder\tTag\tMake\tRun\tCheck\n')
	for ii in range(len(Lfolder)):
		f.write("{}\t{}\t{}\t{}\t{}\n".format(Lfolder[ii], Ltag[ii], Lmake[ii], Lrun[ii], Lcheck[ii]))
	f.close()

#Main
os.chdir(setwd()) #Ustawiamy się w folderze roboczym /home2/scratch/knfk/cold-atoms/testsuite
listOfTests, N = count() # Zapis do listy nazwy testów i ile ich ma być do wykonania
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks, listOfErrors = [], [], [], [], [], []
for i in range(1, N+1):
	os.chdir(setwd()) #Ustawiamy się w folderze roboczym /home2/scratch/knfk/cold-atoms/testsuite
	nameOfTest = str(listOfTests[i-1])
	ifdir = testIsPresent(nameOfTest) #Sprawdza czy dany folder z wypisanych w liście istnieje: zwraca T/F
	ifdesc = testDescIsPresent(nameOfTest, ifdir) #Sprawdza czy w danym folderze, który istnieje jest plik test.desc: zwraca T/F
	#Oba powyższe muszą być ustawione na True, inaczej pętla przejdzie do następnego folderu z następnym testem.
	if ifdir and ifdesc:
		os.chdir(setwd() + '/{}'.format(nameOfTest))
		make, run = runLinuxCommands(os.getcwd())
		listOfMakes.append(make)
		listOfRuns.append(run)
		# Z listy poleceń make mogło się wykonać, ale run niekoniecznie. Run = 'FAIL' jest gdy nie utworzy się plik .cmp
		# więc trzeba sprawdzić czy cmp istnieje, oraz czy .ref istnieje.
		if run == 'FAIL' or not refFile(os.getcwd()):
			listOfChecks.append('FAIL')
		else:
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
logging.info("Zakończenie programu.")
print("--- %.8s seconds ---" % (time.time() - start_time))
