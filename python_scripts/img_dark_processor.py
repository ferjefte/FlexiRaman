#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:42:06 2023

DARK BACKGROUND CORRECTION OF RAW NEON LAMP SPECTRUM IMAGES

@author: fernandoaguila
"""

import numpy as np
import os

def img_dark_pross(img_nf, img_nf_dark, img_f, img_f_dark, dark_corrected_name, nf_dark_corrected_name, f_dark_corrected_name, directory):
    
    # SUBSTRACTION OF DARK BACKGROUND
    img_nf_c = np.int32(img_nf)-np.int32(img_nf_dark)
    img_f_c  =np.int32(img_f)-np.int32(img_f_dark)
    
    # FUSING TWO PARTS OF THE SPECTRUM
    img = img_nf_c+img_f_c
    
    # NEGATIVE VALUES CLIPPING
    img_nf_c[img_nf_c<0] = 0
    img_f_c[img_f_c<0] = 0
    img[img<0] = 0
    
    # OPTION OF SAVING
    dark_corrected_directory = os.path.join(directory, dark_corrected_name)
    np.save(dark_corrected_directory, img)
    
    nofilter_dark_corrected_directory = os.path.join(directory, nf_dark_corrected_name)
    np.save(nofilter_dark_corrected_directory, img_nf_c)
    
    filter_dark_corrected_directory = os.path.join(directory, f_dark_corrected_name)
    np.save(filter_dark_corrected_directory, img_f_c)
    
    return img, img_nf_c, img_f_c
    