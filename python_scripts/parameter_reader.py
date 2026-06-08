# -*- coding: utf-8 -*-
"""
Created on Fri May 23 10:23:24 2025

PROGRAM TO READ THE PARAMETER FROM TXT. FILES
TWO CASES HAD TO BE IMPLEMENTED FOR THE OPTIMIZED PARAMETERS AND FOR THE 
ADJUSTMENTS TO THE SLIT. THE ORDER OF THE PARAMETERS IN THE SLIT ADJUSTMEN FILE 
IS IMPORTANT, NAMELY, yi0-rot-xi0.

@author: aguilafernando
"""
import chardet

def parameter_reader(directory):
    
    # detect the right encoding to open the file
    with open(directory, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    with open(directory, 'r', encoding=encoding) as file:
        # variables = dict(line.strip().split('\t') for line in file if line.strip())
        lines = [l.strip() for l in file if len(l.split('\t'))>=2]
        # print(f'{lines}\n')
        vals = {}
        for l in lines:
                a=l.split('\t')
                print(a)
                vals[a[0]]=a[1]
    
    return vals
            

def parameter_reader_slit(directory):
    
    # detect the right encoding to open the file
    with open(directory, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    with open(directory, 'r', encoding=encoding) as file:
        # variables = dict(line.strip().split('\t') for line in file if line.strip())
        lines = [l.strip() for l in file if len(l.split('\t'))>=2]
        # print(lines)
        vals = {}
        for l in lines:
                a=l.split('\t')
                # print(a)
                if a[0] == 'SLIT':
                    key = a[1]
                    values = []
                else:
                    values.append(a[1])
                    vals[key]=values
    
    return vals