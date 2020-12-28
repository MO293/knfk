import os
# def runLinuxCommands(): # na razie bezargumentowa
#     file = open("test_desc.txt", "r").read().split('\n') #otwiera plik i czyta linia po linii bez enterów
#     line_count = 0 #licznik linii
#     for i in file: # pętla wykonuje się tak długo aż plik ma linie
#         tag, command = i.split(": ") #tworzy 2 stringi nadpisywane co iteracje
#         print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command) #outputuje powyższą listę
#         if i != "\n":
#             line_count += 1
#         if tag == 'tag': #dla tagu "tag" ustawiamy się dla danego testu (nie wiem czy wymagane)
#             os.chdir('C:/Users/user/Desktop/tests/st-test-{}'.format(line_count))
#             print(os.getcwd()) #tego printa na razie zostawiam, by widzieć gdzie na pewno jest
#         if tag == 'exec': #dla tagu "exec" tylko wykonujemy komendę command
#             os.system(command)
#         if tag == 'test': #dla tagu "test" nic nie wykonujemy, tylko sprawdzamy czy istnieją dane outputy
#             if os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
#                 make, run = 'OK', 'OK'
#             elif os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
#                 make, run = 'OK', 'FAIL'
#             elif not os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
#                 make, run = 'FAIL', 'OK'
#             elif not os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
#                 make, run = 'FAIL', 'FAIL'
#             #wartości make i run będą zbierane już do raportu
#     return [make, run]
#         # if tag == 'diff': #dla tagu "diff" sprawdzamy stosunek wartości referencyjnych do outputowych i czy < 10e-3
#         #   generateReport()
# make, run = runLinuxCommands()
# print('Done.')

def runLinuxCommands():
    nowpath = 'C:/Users/maxio/Desktop/testsuite'
    file = open('demofile.txt', "r").read().split('\n')  # otwiera plik i czyta linia po linii bez enterów
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
            if not possible_files: make = 'FAIL'
            else: make = 'OK'
            del possible_files, file_list
            if os.path.exists('test1_cmp.txt'): run = 'OK'
            else: run = 'FAIL'
        if tag == 'diff': pass
    print(dir())
    del command, file, ii, line_count, nowpath, tag
    print(dir())
    return make, run
make, run = runLinuxCommands()
print(make, run)
print(type(make), type(run))