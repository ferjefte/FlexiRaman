#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 11:28:11 2023

@author: fernandoaguila
"""

import os
from fnmatch import fnmatch

def file_path_names(directory, file_format):
    """
    Function that retrieves all the path names of the files in a directory that 
    have the desired file_format

    Parameters
    ----------
    directory : String
        file path where the data is stored.
    file_format : String
        Desired formats of the searched files. For example: "*.txt"

    Returns
    -------
    addresses : List
        List with all the path names of the desired file_format files in directory.

    """

    os.chdir(directory)
    root=os.getcwd()
    pattern = file_format
    addresses=[]
    
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                addresses.append(os.path.join(path, name).lstrip(directory))
                # print(os.path.join(path, name))
    return addresses