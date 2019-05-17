#!/usr/bin/env python3

import argparse
from timeit import default_timer as timer
import random
try:
    import openpyxl
except ModuleNotFoundError:
    print('Paosys.py requires openpyxl. Use "pip install openpyxl" before running program.\n')
    raise SystemExit

def training(excel):
    fast_time = 0
    slow_time = 0
    avg_time = 0
    times = []
    correct = 0
    accuracy = 0
    cols = ['B', 'C', 'D']

    mode = input('Select a mode [pao, pa, po, ao]: ')

    if mode == 'pa':
        cols = ['B', 'C']
    elif mode == 'po':
        cols == ['B', 'D']
    elif mode == 'ao':
        cols == ['C', 'D']
    else:
        print('Not a valid training mode.')
        raise SystemExit

    print('\nDecode the number. Whitespace may be used as seperators.')
    print('Enter q to quit\n') 
    answer = ''
    while(True):
        number, correct_num = gen_num(excel, cols, mode)
        start = timer()
        answer = input('\n' + number + '\n')
        if answer == 'q': break

        end = timer()
        times.append(float(format(end - start,'.2f')))

        answer = ''.join(answer.split())
        if number == encode(excel, answer, mode):
            correct += 1
            print('\nCorrect!\t' + 'Time: ' + str(times[-1]) + '\n\n')
        else:
            print('\nWrong answer. The correct number was: '+ correct_num + '\tTime: ' + str(times[-1]))
            input('Enter to continue')
        
    print('\n\nFasted time: ' + str(min(times)))
    print('Slowest time: ' + str(max(times)))
    print('Average time: ' + str(format(sum(times) / len(times), '.2f')))
    print('Accuracy: ' + str(format(correct / len(times) * 100, '.2f')) + '%\n')
    


def gen_num(excel, cols, mode):
    num = ''
    for i in range(random.randint(17,18)):
        num += str(random.randint(0,9))
    e_num = encode(excel, num, mode)
    return e_num, num 


def replace(excel, args, file_name):
    sheet = excel['Sheet1']

    try:
        number, visual, replace = args
    except ValueError:
        print('Make sure to enclose the replacement association in quotations.\n')
        raise SystemExit

    try:
        int(number)
    except ValueError:
        print('First argument must be a valid number. Use -h to see all options\n')
        raise SystemExit

    if visual not in ['p', 'a', 'o', 'odd']:
        print('Invalid  argument for visual (2nd arg). Try "p", "a", or "o" or use -h to see all options\n')

    col = 'B'
    if visual == 'a':
        col = 'C'
    elif visual == 'o':
        col = 'D'
    elif visual == 'odd':
        col = 'E'

    sheet[col + str(int(number) + 1)] = replace
    file_name = 'pao.xlsx' if not file_name else file_name
    excel.save(file_name)


def encode(excel, num, mode):
    num = ''.join(num.split())
    try:
        int(num)
    except ValueError:
        print('Not a valid number. Use -h to see all options\n')
        raise SystemExit

    chunks = []
    num = list(num)
    encoded = ''
    sheet = excel['Sheet1']
    size = 4 if mode != 'pao' else 6
    col1 = 'B' if mode[0] == 'p' else 'C'
    col2 = 'C' if mode[1] == 'a' else 'D'

    

    while len(num) > 0:
        chunks.append(num[:size])
        num[:size] = []
    
    try:
        for chunk in chunks:
            encoded += ' - ' if encoded != '' else ''
            person = str(int(''.join(chunk[:2]))+1) if len(chunk[:2]) == 2 else str(int(chunk[0])+1)
            encoded += sheet['E' + person].value if len(chunk[:2]) == 1 else sheet[col1 + person].value

            if len(chunk) > 2:
                action = str(int(''.join(chunk[2:4]))+1) if len(chunk[2:4]) == 2 else str(int(chunk[2])+1)
                encoded += ' - ' + sheet['E' + action].value if len(chunk[2:4]) == 1 else ' - ' + sheet[col2 + action].value
            if len(chunk) > 4:
                obj = str(int(''.join(chunk[4:6]))+1) if len(chunk[4:6]) == 2 else str(int(chunk[4])+1)
                encoded += ' - ' + sheet['E' + obj].value if len(chunk[4:6]) == 1 else ' - ' + sheet['D'+ obj].value
    except TypeError:
        print('Error while retrieving data from file. Check your excel file to make sure applicable cells are populated.')
        print('Processed: ', end='')

    return encoded


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-m', dest='mode', default='pao', help='Options: [pa, po, ao, training] (Default: pao)')
parser.add_argument('-n', dest='num', help='The number to be encoded. Use quotations when using whitespace for readability.\n \n' +
    'ex. -n 12345678 -or- -n "1234 5678"\n \n')
parser.add_argument('-f', dest='file', help='Defines alternate file to pull from (Default: pao.xlsx)\n' +
    'Supported formats: .xlsx,.xlsm,.xltx,.xltm')
parser.add_argument('-r', nargs='*', dest='replace', help='Replaces association at assigned spot.\n \n' +
    'Arg 1: Number to be replaced.\nArg 2: Visual to be replaced. Options: [p, a, o, odd].\nArg 3: Replacement association.' +
    '\n \nex. -r 12 p "Abraham Lincoln"\n ')

args = parser.parse_args()

if args.file:
    if args.file[-5:] not in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
        print('Not a supported file format. Supported formats: .xlsx,.xlsm,.xltx,.xltm\n')
        raise SystemExit
        
try:
    excel = openpyxl.load_workbook(args.file) if args.file else openpyxl.load_workbook('pao.xlsx')
except FileNotFoundError:
    print('File not found. Make sure file is in proper directory or file path was typed correctly.\n')
    raise SystemExit

if args.mode == 'training':
    training(excel)
elif args.replace:
    replace(excel, args.replace, args.file)
elif args.num:
    encoded = encode(excel, args.num, args.mode)
    print(encoded + '\n')
else:
    print('No arguments found. Use -h to see available options.\n')
