#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:33:13 2023

FUNCTIONS TO CALCULATE THRESHOLDS ON THE NEON SPECTRUM IMAGE

@author: fernandoaguila
"""
 
import numpy as np
from skimage.filters import threshold_yen, threshold_local

def thres_noise(img):
    """
    
    Function for stablishing the threshold of the image based on the average
    of the negative pixels obtained after correction.

    Parameters
    ----------
    img : numpy.ndarrray 
          Raw data image after dark background correction  

    Returns
    -------
    int
        threshold value.

    """
    m=img.copy()
    m[m>=0]=0
    n=np.sum(m<0)
    #print(f'number of negative pixels:{n}')
    return int((np.sum(-m))/n) 

def thresh_yen(img): 
    """
    Returns the threshold value of the image using the threshold_yen 
    function of skimage.filters package

    Parameters
    ----------
    img : numpy.ndarrray 
          Raw data image after dark background correction 

    Returns
    -------
    int
        threshold yen value.

    """
    
    return threshold_yen(img)

def thresh_local(img): 
    """
    Returns the threshold value of the image using the threshold_local 
    function of skimage.filters package

    Parameters
    ----------
    img : numpy.ndarrray 
          Raw data image after dark background correction 

    Returns
    -------
    int
        threshold local value.

    """
    
    return threshold_local(img)

    
    