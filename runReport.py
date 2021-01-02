# Funkcja generująca raport z przeprowadzonych testów
# Jej output to: user_report_date_time.txt
# Zapis w formacie: Folder|Tag|Make|Run|Check

import os
import datetime
import getpass
def runReport(Lfolder, Ltag, Lmake, Lrun, Lcheck):
    nameReport = getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")
    filepath = 'C:/Users/maxio/Desktop/Pythong/' + nameReport + '.txt'
    if os.path.isfile(filepath):
        os.remove(filepath)
    f = open(filepath, 'w')
    f.write('Folder\tTag\tMake\tRun\tCheck\n')
    for i in range(len(Lfolder)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(Lfolder[i], Ltag[i], Lmake[i], Lrun[i], Lcheck[i]))
    f.close()

#Na potrzeby testów
folder = ['st-test-1', 'st-test-2', 'st-test-3', 'st-test-4', 'st-test-5']
tag = ['test1', 'test2', 'test3', 'test4', 'test5']
make = ['OK', 'OK', 'FAIL', 'OK', 'FAIL']
run = ['OK', 'FAIL', 'OK', 'FAIL', 'FAIL']
check = ['FAIL', 'FAIL', 'OK', 'FAIL', 'FAIL']
runReport(folder, tag, make, run, check)