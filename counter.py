# Funkcja określa jakie testy są do zrealizowania
# Zwraca listę stringów i długość dla tablicy for
import numpy as np

def count():
	testList = np.genfromtxt("tlist.txt", dtype=str)
	return testList, len(testList)

listOfTests, N = count()
print(listOfTests, N)
