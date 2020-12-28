# def report():
# #     # Funkcja główna programu.
# #     # 1.    Porównanie outputów test-i.ref z wygenerowanym test-i.cmp
# #     # 1a.   Wejście do pliku .ref, zczytanie wartości (najlepiej do tablicy/listy)
# #     # 1b.   Wejście do pliku .cmp, zczytanie wartości (najlepiej do tablicy/listy)
# #     # 1c.   Wyznaczenie stosunków wartości cmp/ref (czy mieszczą się w 10e-3), zapisanie wartości stosunków do listy lub
# #     #       opcjonalnie if(<10e-3) zwróć stringa 'OK'.

def runDiffTest():
    listOfValues = []
    with open('test1_cmp.txt') as bf1:
        with open('test1_ref.txt') as bf2:
            for line1, line2 in zip(bf1, bf2):
                cmp_tag, cmp_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z outputu
                ref_tag, ref_value = line1.split(": ") #tworzymy 2 stringi: tag i wartość z referencyjnego
                listOfValues.append(float(cmp_value.rstrip('\n')) - float(ref_value.rstrip('\n')))
                if all(comparedValue < 10e-3 for comparedValue in listOfValues): now_check = 'OK'
                else: now_check = 'FALSE'
    return now_check
