import datetime
import getpass
import logging
import numpy as np
import os
import time
import subprocess as sub

start_time = time.time()
listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfDiffs, listOfChecks, listOfErrors = [], [], [], [], [], [], []

# Setting default working directory
def get_global_dir():
    ggd = os.getcwd()
    return ggd

# Reading the text file with a list of directories with given tests to perform
def count_dirs():
    folder_list = list(np.genfromtxt("tlist.txt", dtype=str, comments="#"))
    return folder_list, len(folder_list)

# Checking if directory with given tests exists in working directory
def check(aa):
    if os.path.exists(aa):
        return True
    else:
        return False

# Checking if test.desc exists
def check_desc(dd="test_desc.txt"):
    if os.path.exists(dd):
        return True
    else:
        return False

# Counting the amount of tests to perform from each test.desc file
def count_tests():
    file = open('test_desc.txt', 'r').read().split('\n')
    amnt = sum([1 for line in file if line.startswith('tag:')])
    return amnt

# Comparing output file to the reference file (value by value)
# If all differences of each values are below given tolerance, test is 'OK'
def run_diff_test(output, reference):
    out_vals, ref_vals, ref_tols, comparedValues = [], [], [], []
    with open(output) as f1:
        next(f1)  # Ta linijka pozwala ominąć tytuły kolumn w plikach
        for line1 in f1:
            out_tag, out_value = line1.split()
            out_vals.append(float(out_value.rstrip('\n')))
    with open(reference) as f2:
        next(f2)
        for line2 in f2:
            ref_tag, ref_value, ref_tolerance = line2.split()
            ref_vals.append(float(ref_value.rstrip('\n')))
            ref_tols.append(float(ref_tolerance.rstrip('\n')))
    for i in range(len(out_vals)):
        if abs(out_vals[i] - ref_vals[i]) < ref_tols[i]:
            comparedValues.append(True)
        else:
            comparedValues.append(False)
    if all(values is True for values in comparedValues):
        now_check = 'OK'
    else:
        now_check = 'FAIL'
    return now_check

# Executing Unix commands given for each test in test.desc file
def commands():
    tag_test_counter = 0
    tab_checks, tab_makes, tab_runs, tab_diffs = [], [], [], []
    file = open('test_desc.txt', "r").read().split('\n')
    for line in file:
        if line.startswith('#'): continue
        if line.startswith('tag:'):
            tagg, add_tag = line.split(': ')
            listOfTags.append(add_tag)
            continue
        if line.startswith('exec:'):
            tagg, ex_comm = line.split(': ')
            os.system(ex_comm)
            continue
        if line.startswith('test:'):
            tag_test_counter += 1
            if tag_test_counter == 1:
                tagg, made_file = line.split(': ')
                if os.path.exists(made_file):
                    now_make = 'OK'
                else:
                    now_make = 'FAIL'
                continue
            if tag_test_counter == 2:
                tagg, out_file = line.split(': ')
                if os.path.exists(out_file):
                    now_run = 'OK'
                else:
                    now_run = 'FAIL'
                tag_test_counter = 0
                continue
        if line.startswith('diff:'):
            tagg, diff_comm = line.split(': ')
            files_to_compare = diff_comm.split(' ')
            file1, file2 = files_to_compare[0], files_to_compare[1]
            if os.path.exists(file1) and os.path.exists(file2):
                check_diff = run_diff_test(file1, file2)
                now_check = str(check_diff)
                tab_checks.append(now_check)
            else:
                now_check = 'FAIL'
                tab_checks.append(now_check)
            tab_makes.append(str(now_make))
            tab_runs.append(str(now_run))
        if len(line) == 0: continue
    return tab_makes, tab_runs, tab_checks

# Generating final report
def runReport(Folder, Tag, Make, Run, Check):
    max_arr = []
    tmp_arr = [Folder, Tag, Make, Run, Check]
    for i in tmp_arr:
        max_arr.append(len(max(i, key=len)))
    space = max(max_arr) + 2
    Folder.insert(0, 'Folder')
    Tag.insert(0, 'Tag')
    Make.insert(0, 'Make')
    Run.insert(0, 'Run')
    Check.insert(0, 'Check')
    filepath = S + '/' + getpass.getuser() + '_report_' + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M") + '.txt'
    arrs = np.transpose([Folder, Tag, Make, Run, Check])
    np.savetxt(filepath, arrs, '%-{}s'.format(space), '\t')

# Cute print to the Terminal window
def cute_print():
    print('\n')
    printable_array = [listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks]
    col_width = max(len(word) for row in printable_array for word in row) + 2
    for row in printable_array:
        print("".join(word.ljust(col_width) for word in row))
    print('\n')


# Main function
S = get_global_dir()  # Set head directory
F, N = count_dirs()  # Amount and names of tests to perform
for folder in F:
    os.chdir(S)  # Return to the head directory after each iteration
    s = os.getcwd()  # Entering to the dir with tests inside to perform
    f = str(folder)
    check_if_dir_exists = check(f)  # Checking if dir with tests exists
    if check_if_dir_exists:
        os.chdir(s + '/{}'.format(f))
        check_desc_file = check_desc()  # Checking if test.desc file exists
        if check_desc_file:
            amount = count_tests()  # Counting tags starting with "tag" from test.desc file.
                                    # It returns the amount of tests in each dir
            for test in range(amount):
                listOfFolders.append(f)
            makes, runs, checks = commands()  # EXECUTING TESTS
            for m in makes: listOfMakes.append(m)
            for r in runs: listOfRuns.append(r)
            for c in checks: listOfChecks.append(c)
        else:
            # Należy dodać logger, informujący, że w folderze ,,folder'' nie znaleziono pliku test.desc
            # więc dany folder został ominięto
            continue
    else:
        # Należy dodać logger, informujący, że dla iteracji ,,folder'' nie znaleziono w folderze roboczym testsuite
        # faktycznego folderu, który zadeklarowano w tlist.txt
        # Należy dodać logger, że dany folder ominięto.
        continue

runReport(listOfFolders, listOfTags, listOfMakes, listOfRuns, listOfChecks)
cute_print()
print('Done.')
print("--- %.8s seconds ---" % (time.time() - start_time))
