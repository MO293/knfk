# Funkcja wchodzi do obu plików, zczytuje wartości z pliku .cmp, potem z pliku .ref
# razem z tolerancjami. Następnie sprawdza, czy wszystkie różnice są mniejsze od tolerancji
# Jeżeli wszystkie są mniejsze to check = OK, jeżeli któraś jest większa to cały check = FALSE.

def runDiffTest():
    valsCmp, valsRef, valsTol, comparedValues = [], [], [], []
    with open('trzy/test1_cmp.txt') as f1:
        next(f1)
        for line1 in f1:
            cmp_tag, cmp_value = line1.split()
            valsCmp.append(float(cmp_value.rstrip('\n')))
    with open('trzy/test1_ref.txt') as f2:
        next(f2)
        for line2 in f2:
            ref_tag, ref_value, ref_tolerance = line2.split()
            valsRef.append(float(ref_value.rstrip('\n')))
            valsTol.append(float(ref_tolerance.rstrip('\n')))
    for i in range(len(valsCmp)):
        if abs(valsCmp[i] - valsRef[i]) < valsTol[i]:
            comparedValues.append('OK')
        else: comparedValues.append('FALSE')
    if all(values == 'OK' for values in comparedValues): now_check = 'OK'
    else: now_check = 'FALSE'
    return now_check