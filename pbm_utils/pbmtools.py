#!/usr/bin/env python3
# PBMtools
# Infected
#    &
# Minorias

from os import remove
import sys

VERBOSE = False

def match_size(f):
    """
    match_size(file) -> right sized bitmap from the pbm file
    """
    line = f.readline().replace('\n','')
    if line != 'P1': # PBM signature check
        print('Format: Error', file=sys.stderr)
        exit()
    else:
        print('Format: OK', file=sys.stderr)

    check = True

    while check:
        line = f.readline().replace('\n','')
        if line != '':
            if line.lstrip()[0] == '#': # PBM author comments
                print(line, file=sys.stderr)
            else:
                check = False
                dimension = list(map(int, line.split()))
                # Dimentions of the pbm matrix
                if dimension <= [64,16]:
                    print('Dimensions: OK (led matrix)', file=sys.stderr)
                else:
                    print('Dimensions: Warning (not compatible with led matrix)', file=sys.stderr)

                return arrange(f.read(), dimension)


def arrange(lines, dimension):
    """
    arrange(lines, (dimension)) -> turns raw data lines into
    a matrix of size dimension[1] * dimension[0] <-> (height * width)
    returns a string with new lines as delimiteers
    """
    bitmap = ['']
    count = 0
    lines = lines.replace('\n', '')
    for i in range(0, dimension[1]):
        for j in range(0, dimension[0]):
            bitmap[i] += lines[count]
            count += 1
        bitmap[i] += '\n'
        bitmap.append('')
    if VERBOSE:
        for i in bitmap:
            print(i, end='', file=sys.stderr)

    return ''.join(bitmap)

def clean_pbm(file_in, file_out):
    """
    clean_pbm(file_in, file_out)
    file_in -> good shit >> file_out
    calls match_size(file_in)
    """
    try:
        fi = open(file_in, 'r')
    except FileNotFoundError:
        print('Error: file not found')
    else:
        fo = open(file_out, 'w')
        fo.write(match_size(fi))
        fi.close()
        fo.close()

def convert_to_pbm(data, file_name, dimension):
    """
    convert_to_pbm(data, file_name, dimension) -> .pbm file
    data must be a bitmap string, file_name the
    future file (without extension) and dimension a tuple (width, height)
    """
    fo = open(file_name+'.pbm', 'w')
    fo.write('P1\n')
    fo.write('# PBMtools v1.2 by Infected and Minorias\n')
    fo.write(str(dimension[0]) + ' ' + str(dimension[1]) + '\n')
    for i in data:
        fo.write(i)
    fo.write('\n')
    fo.close()

if __name__ == '__main__':
    print('Nope', file=sys.stderr)