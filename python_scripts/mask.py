#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:20:57 2023

@author: fernandoaguila
"""

from skimage.filters import threshold_yen
from threshold import thres_noise 
import scipy.ndimage as ndimage

def mask_maker(img_filter, img_nofilter, man_thresh_filter=65, man_thresh_nofilter=1000, man_thresh_view=80):
    """
    Function that calculates the mask out of the corrected spectra raw images with filter and no filter

    Parameters
    ----------
    img_filter : Array of int32
        corrected neon lamp spectral image with the band pass filter.
    img_nofilter : Array of int32
        corrected neon lamp spectral image without the band pass filter.
    man_thresh_filter : int, optional
        Value of the threshold for the spectal image with filter. The default is 300.
    man_thresh_nofilter : int, optional
        Value of the threshold for the spectal image without filter. The default is 1000.
    man_thresh_view : int, optional
        Value of the threshold for the mask for a better spectral lines visualization. The default is 80.

    Returns
    -------
    mask : Array of bool
        Final mask of the whole range of spectral lines.
    mask_plot : Array of bool
        Final mask of the whole range of spectral lines with a lower threshold for visualization of the low intensity lines

    """
    
    
    # CALCULATING THRESHOLD
    # thresh_yesf = thres_noise(img_filter) # own function
    # # print(f'\nThreshold for homogeneous ilumination in image with filter is: {thresh_yesf}')
    # threshy_yesf = threshold_yen(img_filter) # skimage Yen function
    # # print(f'Yen Threshold for homogeneous ilumination in image with filter is: {threshy_yesf}')

    # thresh_nof = thres_noise(img_nofilter) # own function
    # # print(f'\nThreshold for homogeneous ilumination in image no filter is: {thresh_nof}')
    # threshy_nof = threshold_yen(img_nofilter) # skimage Yen function
    # # print(f'Yen Threshold for homogeneous ilumination in image no filter is: {threshy_nof}')
    
    # CALCULATING MASK
    mask_yesf = img_filter> man_thresh_filter
    # mask_yesf_yen = img_filter>threshy_yesf
    # print('\nCurrent own trheshold used for image with filter:', man_thresh_filter)

    mask_nof = img_nofilter> man_thresh_nofilter
    # mask_nof_yen = img_nofilter>(threshy_nof)
    # print('Current trheshold used for image no filter:', m)

    # FUSION OF BOTH MASKS
    mask = mask_yesf+mask_nof
    
    # EXPANDING THE HOLES
    struct = ndimage.generate_binary_structure(2,2)
    mask_dilated = ndimage.binary_dilation(mask, struct)
    
    # mask used for viewing purposes
    mask_plot=(img_filter>man_thresh_view)+mask_nof

    
    
    return mask, mask_dilated