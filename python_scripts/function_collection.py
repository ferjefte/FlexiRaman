#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:16:55 2023

@author: fernandoaguila
"""

# Function to read data from file

import os
import numpy as np
import matplotlib.pylab as plt
from fnmatch import fnmatch
from file_path_names import *
from data_pross_witec_func import *
from scipy.interpolate import *
import tifffile as tiff


def read_data(path, file_ext='*.txt', data_type="witec", method="batch", laser_line=532, x_new=False, filter_cut=False, fname_ext=".txt"):
    
    
    
    os.chdir(path)
    L=file_path_names(path, file_ext)
    Results_dic={}
    # Choice of method (string split for ordering of labels necessary?)
    if method=="batch":
        f=lambda s: np.array([i.split("/") for i in s])
        tmp=f(L)
        if len(tmp[0])!=3:
            raise Exception("Incorrect folder structure")
        L_fn=tmp[::,1]
    elif method=="single":
        L_fn=np.array(L)
        if len(L_fn)==0:
            raise Exception("Wrong filename extension (standard: fnam.ext=\".txt\")!")
    elif method=="single.cal":
        f=lambda s: np.array([i.split("/") for i in s])
        tmp=f(L)
        if len(tmp[0])!=2:
            raise Exception("Incorrect folder structure")
        L_fn=tmp[::,1]
    elif method=="flex":
        L_fn=np.array(L)
    else :
        raise ValueError("Choose valid method!")
    
    #performing ordering
    L=sorted(L)
    Results_dic['Files']=L
    
    #read in / generatte x-axis
    if x_new==False:
        if data_type=="witec":
            x_new=read_witec(L[0])['x']
            Results_dic['x_new']=x_new
    
    
        if filter_cut!=False:
            x_new=x_new[filter_cut<x_new]
            Results_dic['x_new']=x_new
        
    else :
        x_range=np.linspace(0,len(x_new))
        
    # Read in signal (matrix)
    if data_type=='witec':
        y_temp=np.array([read_witec(L[i])['y'] for i in range(len(L))])
        
    # Spline interpolation applied to signal matrix
    
    y=CubicSpline(x_new, y_temp, axis=1)
    Results_dic['y']=y(x_new)
    
    # Generating of label and batch vector 
    
    tmp_2=f( L)
    
    Results_dic['Lab']=tmp_2[::,1]
    Results_dic['Batch']=tmp_2[::,0]
    
    # Calculating the mean and the std of the data
    
    Results_dic['mean']=mean_spec(y(x_new), tmp_2[::,1])
    
    return Results_dic
            

def mean_spec(x, Lab):
    """
    Function to calculate the mean and the standard deviation of the data "x"

    Parameters
    ----------
    x : numpy (n,m) Array 
        Matrix with the signal data.
    Lab : string array
        Array with the names of the folders containing the data read.

    Returns
    -------
    res_dic : Dictionary
        Dictionary containing the mean values, the standar deviation and the labels corresponding to 
        each row of the mean matrix.

    """
    
    labels=sorted(list(set(Lab)))
    m,n=np.shape(x)
    l=len(labels)
    
    res_dic={}
    Mean=np.empty((l,n))
    Std=np.empty((l,n))
    for i in range(l):
        indices=np.where(Lab==labels[i])
        Mean[i,::]=np.mean(x[indices,::], axis=1)
        Std[i,::]=np.std(x[indices,::], axis=1)
    res_dic['labels']=np.array(labels)
    res_dic['mean']=Mean
    res_dic['std']=Std
    return res_dic
    

def read_measurements_pbirms(directory, file_ext='*.tif', n=2048, m=2048):
    
    
    with os.scandir(directory) as entries:
        image_content = [entry.name for entry in entries if fnmatch(entry.name, file_ext)]
    
    # dictionary for the results
    img_dic={}
    
    l=len(image_content)
            
    # create an empty matrix to save all the measured images
    img_msr=np.empty( ( n,m,l ) )
    
    # reading the measurement images and storing them in the empty matrix
    for j in range(l):
        img_path = os.path.join(directory, image_content[j])
        img = np.array( tiff.imread(img_path) )
        img_msr[:,:,j]= img
        
    img_dic['images']=img_msr
    img_dic['avg_imgs']=np.mean(img_msr, axis=2)
        
    return img_dic
    
    
    
    
    
            
            