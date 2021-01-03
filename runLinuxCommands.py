# Funkcja czyta plik z instrukcją test_desc, po czym wykonuje linia po linii każdą komendę.

import os
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
            del possible_files, file_list
            if os.path.exists('test1_cmp.txt'): now_run = 'OK'
            else: now_run = 'FAIL'
        if tag == 'diff': pass
    return now_make, now_run