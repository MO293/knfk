import datetime
import getpass
import logging
import numpy as np
import os
import time
import subprocess as sub

start_time = time.time()
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfDiffs, listOfChecks, listOfErrors = [], [], [], [], [], [], []

# Funkcja ustawia sobie domyślną ścieżkę
def get_global_dir():
    ggd = os.getcwd()
    return ggd

# Funkcja czyta listę z folderami, które zawierają kolejne testy do wykonania
def count_dirs():
    folder_list = list(np.genfromtxt("tlist.txt", dtype=str, comments="#"))
    return folder_list, len(folder_list)

# Funkcja sprawdza czy dany folder istnieje w katalogu roboczym
def check(aa):
    if os.path.exists(aa): return True
    else: return False

# Funkcja sprawdza czy istnieje test.desc
def check_desc(dd="test_desc.txt"):
    if os.path.exists(dd): return True
    else: return False

# Funkcja zlicza, ile testów jest w pliku test.desc
def count_tests():
    file = open('test_desc.txt', 'r').read().split('\n')
    cc = sum([1 for line in file if line.startswith('tag:')])
    return cc

# Funkcja porównująca output do pliku referencyjnego
def run_diff_test(output, reference):
    out_vals, ref_vals, ref_tols, comparedValues = [], [], [], []
    with open(output) as f1:
        next(f1) # Ta linijka pozwala ominąć tytuły kolumn w plikach
        for line1 in f1:
            out_tag, out_value = line1.split()
            out_vals.append(float(out_value.rstrip('\n')))
    with open(reference) as f2:
        next(f2)
        for line2 in f2:
            ref_tag, ref_value, ref_tolerance = line2.split()
            ref_vals.append(float(ref_value.rstrip('\n')))
            ref_tols.append(float(ref_tolerance.rstrip('\n')))
    for i in range(len(out_vals)):
        if abs(out_vals[i] - ref_vals[i]) < ref_tols[i]: comparedValues.append(True)
        else: comparedValues.append(False)
    if all(values is True for values in comparedValues): now_check = 'OK'
    else: now_check = 'FAIL'
    return now_check

# Funkcja wykonująca komendy unixowe
def commands():
    tab_checks, tab_makes, tab_runs, tab_diffs = [], [], [], []
    file = open('test_desc.txt', "r").read().split('\n')
    for line in file:
        if line.startswith('tag:'):
            tagg, comm = line.split(': ')
            listOfTags.append(comm)
            continue
        if line.startswith('exec:'):
            tagg, comm = line.split(': ')
            os.system(comm)
            continue
        if line.startswith('-wslda-', 8):
            file_list = os.listdir()
            possible_files = [fn for fn in file_list if '-wslda-' in fn]
            if possible_files: now_make = 'OK'
            else: now_make = 'FAIL'
            continue
        if line.startswith('test:'):
            tagg, iffile = line.split(': ')
            if os.path.exists(iffile): now_run = 'OK'
            else: now_run = 'FAIL'
            continue
        if line.startswith('diff:'):
            tagg, comm = line.split(': ')
            compfiles = comm.split(' ')
            file1, file2 = compfiles[0], compfiles[1]
            if os.path.exists(file1) and os.path.exists(file2):
                check_diff = run_diff_test(file1, file2)
                tab_checks.append(str(check_diff))
            else: tab_checks.append('FAIL')
            tab_makes.append(str(now_make))
            tab_runs.append(str(now_run))
            continue
        if len(line) == 0: continue
    return tab_makes, tab_runs, tab_checks

# Funkcja generująca raport
def runReport(Lfolder, Ltag, Lmake, Lrun, Lcheck):
    filepath = S + '/' + getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M") + '.txt'
    ff = open(filepath, 'w')
    ff.write('Folder\tTag\tMake\tRun\tCheck\n')
    for ii in range(len(Lfolder)):
        ff.write("{}\t{}\t{}\t{}\t{}\n".format(Lfolder[ii], Ltag[ii], Lmake[ii], Lrun[ii], Lcheck[ii]))
    how_many = len(list(set(Lfolder)))
    perc = how_many * 100 // N
    ff.write('\n')
    ff.write('Operacje przeprowadzono na ' + str(how_many) + '/' + str(N) + ' folderach, co daje wykonanie rowne ' + str(perc) + ' procent [%].')
    ff.close()

def cute_print():
    print('\n')
    listOfFolders.insert(0, 'Folders')
    listOfTags.insert(0, 'Tag')
    listOfMakes.insert(0, 'Make')
    listOfRuns.insert(0, 'Run')
    listOfChecks.insert(0, 'Check')
    printable_array = [listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks]
    col_width = max(len(word) for row in printable_array for word in row) + 2
    for row in printable_array:
        print("".join(word.ljust(col_width) for word in row))
    print('\n')
# Main
S = get_global_dir()
os.chdir(S)
F, N = count_dirs()  # Zapis do listy nazwy testow i ile ich ma byc do wykonania
for folder in F:
    os.chdir(S) #Ustawiamy się w folderze roboczym co iterację
    s = os.getcwd() #Inicjujemy zmienną położeniową co iterację
    f = str(folder)
    check_if_dir_exists = check(f) #Sprawdzamy czy folder istnieje
    if check_if_dir_exists: # Jeżeli folder istnieje
        os.chdir(s + '/{}'.format(f)) # to wchodzimy do danego folderu
        check_desc_file = check_desc() # Sprawdzamy w nim czy istnieje test.desc
        if check_desc_file: # Jeżeli test.desc w nim istnieje
            amount = count_tests() # to zliczane są tagi, które dadzą informację o ilości testów do wykonania
            for a in range(amount): # Dla każdego TAG-testu
                listOfFolders.append(f) # do listy folderów dodajemy folder
            makes, runs, checks = commands() # Wykonujemy testy
            for m in makes: listOfMakes.append(m)
            for r in runs: listOfRuns.append(r)
            for c in checks: listOfChecks.append(c)
        else:
            # Należy dodać logger, informujący, że w folderze ,,folder'' nie znaleziono pliku test.desc
            # więc dany folder został ominięto
            continue
    else:
        # Należy dodać logger, informujący, że dla iteracji ,,folder'' nie znaleziono w folderze roboczym testsuite
        # faktycznego folderu, który zadeklarowano w tlist.txt
        # Należy dodać logger, że dany folder ominięto.
        continue


cute_print()
runReport(listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks)
print('Done.')
print("--- %.8s seconds ---" % (time.time() - start_time))