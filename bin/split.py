#!/usr/bin/env python
import csv
from collections import namedtuple
import logging
import os
import sys
import yaml

filepath=os.path.realpath(sys.argv[1])
filename=os.path.basename(filepath)
folder = os.path.dirname(filepath)
config_file = os.path.realpath('%s/../conf/split.yaml' %os.path.dirname(__file__))

with open(config_file) as f:
    config = yaml.safe_load(f)

csv_rows = config['csv_rows']

def padd_empty(L):
    padd = ''
    for i in xrange(len(L)):
        if L[i] != '':
            padd=L[i]
        else:
            L[i]=padd

#TODO: next
def select_values(d, L, values):
    ret = dict()
    for val in values:
        ret[val]=[L[i] for i in d[val]]
    return ret

def select_indices(d, L, values):
    for val in values:
        d[val]=[i for i, x in enumerate(header1) if x == val]

def merge_dict(d,L):
    pass

def remove_chars(L,chars):
    for i in xrange(len(L)):
        for c in chars:
            c=L[i].replace(c,'')
            try:
                c=float(c)
            except ValueError:
                pass
            L[i]=c

def short_instance(groups,s):
    group,_,s=s.split('/')
    try:
        group=config['short_groups'][group]
    except KeyError:
        logging.warn('No short form for Group "%s"' %group)
    try:
        groups[group].add(s)
    except KeyError:
        groups[group]=set([s])
    s = len(groups[group])
    return [group, s]


with open(filepath, 'rb') as csvfile:
    csv_data = csv.reader(csvfile, dialect='excel')
    header0 = csv_data.next()
    header0=filter(lambda x: x!='', header0)
    header1 = csv_data.next()
    header1[0]='set'
    
    for i in xrange(len(header0)):
        for k,v in config['csv_header'].iteritems():
            header0[i]=header0[i].replace(k,v)
        header0[i]=header0[i].replace('-','_').replace(' ', '')
        
    rows = dict()
    select_indices(rows,header1,csv_rows)
    res=dict()
    for i in csv_rows: res[i]=[header0]
    groups=dict()
    for line in csv_data:
        remove_chars(line,[','])
        vals = select_values(rows,line,csv_rows)
        for k in vals:
            try:
                res[k].append(short_instance(groups,line[0]) + vals[k])
            except ValueError:
                logging.error('No Value "%s". Ignoring line...' %line[0])
                continue

    for r in csv_rows:
        res[r][0].insert(0,'set')
        res[r][0].insert(1,'#')
        break

    for row in csv_rows:
        with open('%s/%s_%s.csv' %(folder,filename,row), 'w') as out:
            csv_out = csv.writer(out, dialect='excel')
            csv_out.writerows(res[row])
