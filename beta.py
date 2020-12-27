import os

#Funkcja ustawia ścieżkę na testsuite i zlicza ile jest w nich folderów (testów st/td) do wykonania
def amountOfDirs():
    os.chdir('C:/Users/maxio/Desktop/testsuite')
    workPath = os.getcwd()
    return int(len(next(os.walk(workPath))[1]) / 2)  # funkcja zliczająca foldery

#Funkcja sprawdza czy dany st-test-i istnieje
def ifStExists(wd, i):
    if os.path.exists(str(wd) + str("/st-test-{}".format(i))):
        return True
    else:
        return False

#Funkcja sprawdza cy dany td-test-i istnieje
#Możliwość sklejenia w jedną funkcję sprawdzającą czy test-i istnieje
def ifTdExists(wd, i):
    if os.path.exists(str(wd) + str("/td-test-{}".format(i))):
        return True
    else:
        return False

#Funkcja wywołująca komendy z pliku test_desc
def runLinuxCommands():
    def runTest():  # na razie bezargumentowa
        file = open("test_desc.txt", "r").read().split('\n')  # otwiera plik i czyta linia po linii bez enterów
        line_count = 0  # licznik linii
        for i in file:  # pętla wykonuje się tak długo aż plik ma linie
            tag, command = i.split(": ")  # tworzy 2 stringi nadpisywane co iteracje
            print('Linia nr ' + str(line_count) + ' zawiera komendę: ' + command)  # outputuje powyższą listę
            if i != "\n":
                line_count += 1
            if tag == 'tag':  # dla tagu "tag" ustawiamy się dla danego testu (nie wiem czy wymagane)
                os.chdir('C:/Users/user/Desktop/tests/st-test-{}'.format(line_count))
                print(os.getcwd())  # tego printa na razie zostawiam, by widzieć gdzie na pewno jest
            if tag == 'exec':  # dla tagu "exec" tylko wykonujemy komendę command
                os.system(command)
            if tag == 'test':  # dla tagu "test" nic nie wykonujemy, tylko sprawdzamy czy istnieją dane outputy
                if os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
                    make, run = 'OK', 'OK'
                elif os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
                    make, run = 'OK', 'FAIL'
                elif not os.listdir().count('myEmptyFile.txt') and os.listdir().count('test1.txt'):
                    make, run = 'FAIL', 'OK'
                elif not os.listdir().count('myEmptyFile.txt') and not os.listdir().count('test1.txt'):
                    make, run = 'FAIL', 'FAIL'
                # wartości make i run będą zbierane już do raportu
        return [make, run]
        # if tag == 'diff': #dla tagu "diff" sprawdzamy stosunek wartości referencyjnych do outputowych i czy < 10e-3
        #   runDiffTest()

#Funkcja porównująca wartości outputowe cmp z referencyjnymi ref
def runDiffTest():
    listOfValues = []
    with open('test1_cmp.txt') as bf1:
        with open('test1_ref.txt') as bf2:
            for line1, line2 in zip(bf1, bf2):
                cmp_tag, cmp_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z outputu
                ref_tag, ref_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z referencyjnego
                cmp_value = float(cmp_value.rstrip('\n')) #str to float
                ref_value = float(ref_value.rstrip('\n')) #str to float
                listOfValues.append('OK')  #sprawdzamy czy wartość check do raportu ma być OK czy FAIL
    return print(all(check == 'OK' for check in listOfValues))

#Funkcja generująca raport
def report(folder, tag, make, run, check):
    filepath = 'C:/Users/maxio/Desktop/tests/NowyOutput.txt' #home2/archive/....
    if os.path.isfile(filepath):
        os.remove(filepath)
    f = open(filepath, 'w')
    f.write('Folder\tTag\tMake\tRun\tCheck\n')
    for i in range(len(folder)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(folder[i], tag[i], make[i], run[i], check[i]))
    f.close()

#Main
N = amountOfDirs(setwd)
print(N)

