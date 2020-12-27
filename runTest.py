import os
def runTest(): # na razie bezargumentowa
    file = open("test_desc.txt", "r").read().split('\n') #otwiera plik i czyta linia po linii bez enterów
    line_count = 0 #licznik linii
    for i in file: # pętla wykonuje się tak długo aż plik ma linie
        tag, command = i.split(": ") #tworzy 2 stringi nadpisywane co iteracje
        print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command) #outputuje powyższą listę
        if i != "\n":
            line_count += 1
        if tag == 'tag': #dla tagu "tag" ustawiamy się dla danego testu (nie wiem czy wymagane)
            os.chdir('C:/Users/user/Desktop/tests/st-test-{}'.format(line_count))
            print(os.getcwd()) #tego printa na razie zostawiam, by widzieć gdzie na pewno jest
        if tag == 'exec': #dla tagu "exec" tylko wykonujemy komendę command
            os.system(command)
        if tag == 'test': #dla tagu "test" nic nie wykonujemy, tylko sprawdzamy czy istnieją dane outputy
            if os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
                make, run = 'OK', 'OK'
            elif os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
                make, run = 'OK', 'FAIL'
            elif not os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
                make, run = 'FAIL', 'OK'
            elif not os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
                make, run = 'FAIL', 'FAIL'
            #wartości make i run będą zbierane już do raportu
    return [make, run]
        # if tag == 'diff': #dla tagu "diff" sprawdzamy stosunek wartości referencyjnych do outputowych i czy < 10e-3
        #   generateReport()
make, run = runTest() #myślę że będzie zwracać od razu argumenty przekazywane do raportu
print('Done.')
