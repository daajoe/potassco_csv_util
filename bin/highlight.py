#!/usr/bin/env python
import argparse
import csv
import logging
import os
import sys
import yaml

parser = argparse.ArgumentParser(description='Highlight max/min lines in CSV.')
parser.add_argument('--max', dest='max', action='store_const',
                    const=max, default=None, help='highlight max by +')
parser.add_argument('--min', dest='min', action='store_const',
                    const=min, default=None, help='highlight max by -')
parser.add_argument('--skip-line', metavar='skip_line', type=int, default=1, 
                    help='#lines to skip (e.g., header)')
parser.add_argument('--skip-row', metavar='skip_row', type=int, default=2,
                    help='#rows to skip (e.g., header)')
#parser.add_argument('filename', metavar='filename', type=str,
#                    help='FILE')

args = parser.parse_args()
#filepath = os.path.realpath(args.filename)

highlight=filter(lambda x: x[0] is not None, [(args.max,'+'), (args.min,'-')])

def get_highlighted(L,F):
    m = []
    for f,h in F:
        val = f(L)
        m.append([i for i, j in enumerate(L) if j == val])
    for j in xrange(len(m)):
        for i in m[j]:
            L[i]='%s%s' %(L[i],F[j][1])
    return L

def main():
#with open(filepath, 'rb') as csvfile:
    csv_data = csv.reader(sys.stdin, dialect='excel')
    res = []
    for i in xrange(args.skip_line):
        res.append(csv_data.next())
    for line in csv_data:
        line[args.skip_row:]=map(float, line[args.skip_row:])
        line[args.skip_row:]=get_highlighted(line[args.skip_row:],highlight)
        res.append(line)
    
    csv_out = csv.writer(sys.stdout, dialect='excel')
    csv_out.writerows(res)


main()
