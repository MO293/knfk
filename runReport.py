# #     # 2.    Wygeneruj raport .csv/.xls/.xlsx/.dat/.txt (nazwy kolumn: folder|tag|make|run|check)
# #     # 3.    Zapisać raport w cd /home2/archive/ (opcjonalnie, nie wiem czy nie będzie on zczytywany szybciej niż 100 dni)

import os
def runReport(folder, tag, make, run, check):
    filepath = 'C:/Users/maxio/Desktop/tests/NowyOutput.txt'
    if os.path.isfile(filepath):
        os.remove(filepath)
    f = open(filepath, 'w')
    f.write('Folder\tTag\tMake\tRun\tCheck\n')
    for i in range(len(folder)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(folder[i], tag[i], make[i], run[i], check[i]))
    f.close()

#Na potrzeby testów
folder = ['st-test-1', 'st-test-2', 'st-test-3', 'st-test-4', 'st-test-5']
tag = ['test1', 'test2', 'test3', 'test4', 'test5']
make = ['OK', 'OK', 'FAIL', 'OK', 'FAIL']
run = ['OK', 'FAIL', 'OK', 'FAIL', 'FAIL']
check = ['FAIL', 'FAIL', 'OK', 'FAIL', 'FAIL']
report(folder, tag, make, run, check)