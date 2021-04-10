import datetime
import getpass
import logging
import numpy as np
import os
import time
import subprocess as sub
#configuration logger in console
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#configuration logger in testsuite.log file
logFilePath=setwd() + getpass.getuser() + 'testsuite' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M") + '.log'
logging.basicConfig(filename=logFilePath,level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#disable all logger comunicates
#logging.disable(logging.CRITICAL)

#testsuiteDirPath="/home2/scratch/knfk/cold-atoms/testsuite"
testsuiteDirPath="/home/dteam011/testsuite"
#makeReportDirPath = "/home2/scratch/knfk/cold-atoms/testsuite"
makeReportDirPath = "/home/dteam011/knfk"
logging.debug("Starting testsuite.")
start_time = time.time()

#setting up default working directory for tests /home2/scratch/knfk/cold-atoms/testsuite
def setwd():
	return testsuiteDirPath

#Tests counting
def count():
	logging.info("Tests counting.")
	testList = list(np.genfromtxt("tlist.txt", dtype=str, comments="#"))
	return testList, len(testList)

#Checking if the test exists
def testIsPresent(testName):
	logging.info("Checking if the \"" + testName + "\" test exists.")
	if os.path.exists(testName):
		listOfFolders.append('{}'.format(testName))
		logging.info("\"" + testName + "\" test found.")
		return True
	else:
		listOfFolders.append(testName)
		listOfTags.append('FAIL')
		listOfMakes.append('FAIL')
		listOfRuns.append('FAIL')
		listOfChecks.append('FAIL')

		logging.info("Test \"" + testName + "\" does not exist.")

	return False

#Checking if there is test_desc file in the given test
def testDescIsPresent(nameOfFolder, folderIsPresent):
	if folderIsPresent:
		os.chdir(setwd()+'/{}'.format(nameOfFolder)) # entering the directory if it exists		
		logging.debug("\"" + str(setwd()+'/{}'.format(nameOfFolder)) + "\" directory opened.")

		if os.path.exists('test.desc'):
			listOfTags.append('OK')
			logging.info("\"test.desc\" file found in \"" + nameOfFolder + "\" directory.")
			return True # return True if test.desc exists
		else: # Otherwise it FAILs for makes/run/checks
			listOfTags.append('FAIL')
			listOfMakes.append('FAIL')
			listOfRuns.append('FAIL')
			listOfChecks.append('FAIL')

			logging.info("\"test.desc\" does not exist in \"" + nameOfFolder + "\" directory.")

			return False
	else:
		logging.info("\"" + nameOfFolder + "\" directory does not exist.") 
		return False

#Checking if there is reference file .ref within a given directory
def refFile(nowpath):
	logging.info("Checking if there is a .ref file.")
	file_list = os.listdir(nowpath)
	possible_files = [fn for fn in file_list if 'ref' in fn]
	if possible_files == []:
		logging.info(".ref file not found.")		
		return False
	
	else: return True

#Executing commands from test_desc file
def runLinuxCommands(nowpath):
	logging.info("Executing commands from \"test.desc\" file.")
	file = open('test.desc', "r").read().split("\n")  #read file line by line without newlines
	line_count = 0 
	for line in file:		
		if len(line) == 0: continue
		else: pass
		tag, command = line.split(": ")  #reading  new tag and command divided by ':' in line
		print('Line num. ' + str(line_count) + ' contains command: ' + command)
		if tag == 'tag': continue # ignore tag 'tag'
		if tag == 'exec':  # execute command
			os.system(command)
			#sub.run(command)
		if tag == 'test':  # checking if the file exists
			file_list = os.listdir(nowpath)
			possible_files = [fn for fn in file_list if '-wslda-' in fn]
			if not possible_files: 
				now_make = 'FAIL'
				logging.info("\"-wslda-\" files not found.")
			else: now_make = 'OK'
			if os.path.exists('test1.cmp'): now_run = 'OK'
			else: 
				now_run = 'FAIL'
				logging.info("\"test1.cmp\" file does not exist.") 
		if tag == 'diff': pass

		line_count += 1

	return now_make, now_run

#Comparing output values from cmp files with reference values
def runDiffTest():
	logging.info("Checking reference values.")
	valsCmp, valsRef, valsTol, comparedValues = [], [], [], []
	with open('test1.cmp') as f1:
		#next(f1)
		logging.info("\"test1.cmp\" opened.")
		for line1 in f1:
			cmp_tag, cmp_value = line1.split()
			valsCmp.append(float(cmp_value.rstrip('\n')))
	with open('ref.test1') as f2:
		logging.info("\"ref.test1\" opened.")
		next(f2)
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

#Generating report
def runReport(Lfolder, Ltag, Lmake, Lrun, Lcheck):
	logging.info("Generating report.")
	filepath = setwd() + getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M") + '.txt'
	#filepath = os.getcwd() + "getpass.getuser()" + '_report_.txt'
	#filepath =makeReportDirPath + '_report_.txt'
	f = open(filepath, 'w')
	f.write('Folder\tTag\tMake\tRun\tCheck\n')
	for ii in range(len(Lfolder)):
		f.write("{}\t{}\t{}\t{}\t{}\n".format(Lfolder[ii], Ltag[ii], Lmake[ii], Lrun[ii], Lcheck[ii]))
	f.close()

#Main
os.chdir(setwd()) #Ustawiamy sie w folderze roboczym /home2/scratch/knfk/cold-atoms/testsuite
#sub.run("pwd") #debug
#sub.run("module load openmpi-gcc721-Cuda90")
#sub.run("module load cuda/9.0x")
#sub.run("source /home/dteam011/testsuite/st-test-1/env.sh")
listOfTests, N = count() # Zapis do listy nazwy testow i ile ich ma byc do wykonania
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks, listOfErrors = [], [], [], [], [], []
for i in range(1, N+1):
	os.chdir(setwd()) #Ustawiamy sie w folderze roboczym /home2/scratch/knfk/cold-atoms/testsuite
	nameOfTest = str(listOfTests[i-1])
	ifdir = testIsPresent(nameOfTest) #Sprawdza czy dany folder z wypisanych w liscie istnieje: zwraca T/F
	ifdesc = testDescIsPresent(nameOfTest, ifdir) #Sprawdza czy w danym folderze, ktory istnieje jest plik test.desc: zwraca T/F
	#Oba powyzsze musza byc ustawione na True, inaczej petla przejdzie do nastepnego folderu z nastepnym testem.
	if ifdir and ifdesc:
		os.chdir(setwd() + '/{}'.format(nameOfTest))
		#print("@@@@@@@@@@PWD@@@@@@@@@@")
		#sub.run("pwd")
		make, run = runLinuxCommands(os.getcwd())
		listOfMakes.append(make)
		listOfRuns.append(run)
		# Z listy polecen make moglo sie wykonac, ale run niekoniecznie. Run = 'FAIL' jest gdy nie utworzy sie plik .cmp
		# wiec trzeba sprawdzic czy cmp istnieje, oraz czy .ref istnieje.
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
logging.info("End of program.")
print("--- %.8s seconds ---" % (time.time() - start_time))
