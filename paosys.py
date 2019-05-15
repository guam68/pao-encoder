import argparse
import openpyxl


def training(excel):
    print('this is training')


def replace(excel, args):
    number, visual, replace = args

    if visual not in ['p', 'a', 'o']:
        print('\nInvalid  argument for visual (2nd arg). Try "p", "a", or "o" or use -h to see all options\n\n')


def encode(excel, num, mode):
    chunks = []
    num = list(num)
    encoded = ''
    sheet = excel['Sheet1']
    size = 4 if mode else 6

    while len(num) > 0:
        chunks.append(num[:size])
        num[:size] = []
    
    for chunk in chunks:
        person = str(int(''.join(chunk[:2]))+1) if len(chunk[:2]) == 2 else str(int(chunk[0])+1)
        encoded += sheet['E' + person].value if len(chunk[:2]) == 1 else sheet['B'+ person].value

        if len(chunk) > 2:
            action = str(int(''.join(chunk[2:4]))+1) if len(chunk[2:4]) == 2 else str(int(chunk[2])+1)
            encoded += sheet['E' + action].value if len(chunk[2:4]) == 1 else sheet['C'+ action].value
            if mode: encoded += '\t'
        if len(chunk) > 4:
            obj = str(int(''.join(chunk[4:6]))+1) if len(chunk[4:6]) == 2 else str(int(chunk[4])+1)
            encoded += sheet['E' + obj].value if len(chunk[4:6]) == 1 else sheet['D'+ obj].value + '\t'



    print(encoded)



parser = argparse.ArgumentParser()

parser.add_argument('-m', dest='mode')
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
    encode(excel, args.num, args.mode)
