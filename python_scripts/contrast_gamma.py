#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:24:06 2023

GAMMA CORRECTION OF IMAGE 

@author: fernandoaguila
"""

# Program to modify the contrast of an image in order to get better contrast on 
# some screens

import numpy as np

def ContrastGamma (ImgIn,min_in,max_in,min_out,max_out,gamma): #raw converter
    #ImgIn:    input image
    #min_in:   minimum input level (to be projected to min_out), typ: cammera dark level or a little higher
    #max_in:   maximum input level (to be projected to min_out), typ: level of brightest region of image
    #min_out:  typ: 0
    #max_out:  typ: 255 or 65535
    #gamma:    use 1 to gain a linear result, use 1/2.2 to compensate for monitor gamma of 2.2
    return (np.clip((ImgIn.astype(np.float32)-min_in)/(max_in-min_in),0,1)**gamma)*(max_out-min_out)+min_out;