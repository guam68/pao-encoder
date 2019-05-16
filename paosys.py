import argparse
import openpyxl
from timeit import default_timer as timer
import random

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


def replace(excel, args):
    number, visual, replace = args

    if visual not in ['p', 'a', 'o']:
        print('\nInvalid  argument for visual (2nd arg). Try "p", "a", or "o" or use -h to see all options\n\n')


def encode(excel, num, mode):
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
    
    for chunk in chunks:
        person = str(int(''.join(chunk[:2]))+1) if len(chunk[:2]) == 2 else str(int(chunk[0])+1)
        encoded += sheet['E' + person].value + ' ' if len(chunk[:2]) == 1 else sheet[col1 + person].value + ' '

        if len(chunk) > 2:
            action = str(int(''.join(chunk[2:4]))+1) if len(chunk[2:4]) == 2 else str(int(chunk[2])+1)
            encoded += sheet['E' + action].value + ' ' if len(chunk[2:4]) == 1 else sheet[col2 + action].value + ' '
        if len(chunk) > 4:
            obj = str(int(''.join(chunk[4:6]))+1) if len(chunk[4:6]) == 2 else str(int(chunk[4])+1)
            encoded += sheet['E' + obj].value + ' ' if len(chunk[4:6]) == 1 else sheet['D'+ obj].value + ' '

    return encoded


parser = argparse.ArgumentParser()

parser.add_argument('-m', dest='mode', default='pao')
parser.add_argument('-n', dest='num')
parser.add_argument('-f', dest='file')
parser.add_argument('-r', nargs='*', dest='replace')

args = parser.parse_args()

try:
    excel = openpyxl.load_workbook(args.file) if args.file else openpyxl.load_workbook('pao.xlsx')
except FileNotFoundError:
    print('\nFile not found\n\n')
    raise SystemExit

if args.num:
    try:
        int(args.num)
    except ValueError:
        print('\nFirst argument must be a valid number. Use -h to see all options\n\n')
        raise SystemExit

if args.mode == 'training':
    training(excel)
elif args.replace:
    replace(excel, args.replace)
else:
    encoded = encode(excel, args.num, args.mode)
    print(encoded)
