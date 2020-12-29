# Funkcja określa jakie testy są do zrealizowania
# Zwraca listę stringów i długość dla tablicy for
def count():
    array = []
    f = open('testlist.txt', 'r').read().split('\n')
    for i in f:
        array.append(i)
    return array, len(array)
listOfTests, N = count()