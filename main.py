######################################
#  Koło Naukowe Fizyki Komputerowej  #
#               WSLDA                #
#           System testujący         #
######################################

import os
# import subprocess
# import pandas

def setWd():
    # Funkcja opcjonalna
    # 1.    Ustawia working directory: /home2/scratch/knfk/cold-atoms/testsuite
    #       żeby mieć pewność, że skrypt wykona się w folderze testsuite.
    os.chdir('C:/Users/user/Desktop/tests')
    return os.getcwd()

def amountOfDir(workpath):
    # 1.    Sprawdza ile testów będzie trzeba wykonać. Forloop chyba zadziała szybciej niż while(),
    #       dlatego fajnie jakby skrypt wiedział z góry ile razy będzie się iterował (wykonywał).
    # 2.    Dzieli przez 2, bo będziemy iterować dla każdego "i" po st-test-i oraz td-test-i
    return int(len(next(os.walk(workpath))[1]) / 2)


def ifStExists(wd, i):
#     # 1.    Funkcja sprawdza czy dany st-test-i/td-test-i istnieje.
#     # 2.    Jeżeli tak: zwraca true, wchodzi do danego testu st/td, wykonują się dalsze operacje.
#     # 3.    Jeżeli nie: zwraca false, zostajemy w testsuite, sprawdzamy czy istnieje następna para st/td-test-i+1
#     # 3a.   Jeżeli istnieje następna para to: punkt 2.
#     # 3b.   Jeżeli nie istnieje następna para to: punkt 3.
#     if path.exists(str(wd) + str("/st-test-{}".format(i))) == True: #tutaj był backslash	(B)
#         return True
#     else:
#         print('Do something else. Najprawdopodobniej będzie wracał do katalogu i szukał następnego testu.')
#         return False
#
#
def ifTdExists(wd, i):
#     if path.exists(str(wd) + str("/td-test-{}".format(i))) == True:
#         return True
#     else:
#         print('Do something else. Najprawdopodobniej będzie wracał do katalogu i szukał następnego testu.')
#         return False
#
def invalidTagIn(line, idx):
# 	status = False
# 	tagList = ["tag", "exec", "test", "diff", "\n"]
# 	tag = line.split(": ")[0]
# 	if not tag in tagList:
# 		print("Unknown tag \"" + tag + "\" in line " + str(idx))
# 		status = True
#
def validationCheck(testFile):
# 	# Funkcja sprawdza czy nie ma żadnych literówek w tagach pliku test.desc
# 	validation = True
# 	for idx, line in enumerate(testFile):
# 		if invalidTagIn(line, idx):
# 			validation = False
# 	return validation
#
#
def runTest():
#     # Funkcja główna programu.
#     # 1.    Otwiera dany folder: st/td-test-i
# 	testDescFile = open("st-test-1/test.desc", "r")
#     # 2.    Czyta instrukcję test.desc określającą kroki testu
# 	validationCheck(testDescFile)
#     # 2a.   Wyczyszczenie folderu z potencjalnych ,,śmieci"
#     # 3.    Część główna: implementacja kroków testu do konsoli dwarf. Każdy exec/test/diff/inne
#     # 3a.   Sprawdzenie czy w folderze st/td-test-i wytworzył się plik wykonywalny. Jeżeli nie, to czy ponawiać czynności? Ile razy?
#     # 3b.   Jeżeli plik wykonywalny istnieje to RUN.
#
#
def runDiffTest():
#     # Funkcja główna programu.
#     # 0.    Sprawdzić czy test1.txt i test1_ref.txt istnieje
#     # 1.    Porównanie outputów test-i.ref z wygenerowanym test-i.cmp
#     # 1a.   Wejście do pliku .ref, zczytanie wartości (najlepiej do tablicy/listy)
#     # 1b.   Wejście do pliku .cmp, zczytanie wartości (najlepiej do tablicy/listy)
#     # 1c.   Wyznaczenie stosunków wartości cmp/ref (czy mieszczą się w 10e-3), zapisanie wartości stosunków do listy lub
#     #       opcjonalnie if(<10e-3) zwróć stringa 'OK'.

def report():
#     # 1.    Wygeneruj raport .csv/.xls/.xlsx/.dat/.txt (nazwy kolumn: folder|tag|make|run|check)
#     # 2.    Zapisać raport w cd /home2/archive/ (opcjonalnie, nie wiem czy nie będzie on zczytywany szybciej niż 100 dni)

def clean():
#     # Funkcja opcjonalna
#     # 1.    Sprzątamy w danym folderze, usuwamy niepotrzebne pliki, program kontynuuje prace na następnym st/td-test-i+1 folderze.

def main():
    #Funkcja wykonywująca algorytm.
    # 1.    Uruchomienie zapętlonych funkcji
    # 2.    Wysłanie raportu
