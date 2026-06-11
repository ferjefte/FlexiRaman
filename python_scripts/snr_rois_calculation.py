# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:48:15 2025

PROGRAM TO CALCULATE THE SNR FROM DIFFERENT REGIONS ON THE IMAGE

FIRST THE ROIs COORDINATES ARE READ FROM .txt FILES
ORDER OF SAVING:
    1) coords_01.txtx  -->  UPPER LEFT
    2) coords_02.txtx  -->  UPPER RIGHT
    3) coords_03.txtx  -->  CENTER
    4) coords_04.txtx  -->  LOWER LEFT
    5) coords_05.txtx  -->  LOWER RIGHT

THE AVERAGE IS CALCULATED FROM THESE ROIs

THEN, BASE LINE CORRETION IS PERFORMED
 

@author: aguilafernando
"""

import os
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pybaselines import Baseline
from pathlib import Path

# FOLDER NAMES AND DIRECTORIES
project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")

date = '20250717'
# date = '20250523'
# date = '20250516'

sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
# sample = 'Pig01_C'
# sample = 'Volt'

ROI = '03'

test = '01'

# subfolder = r"2025-08-11_19-35-21_c5" # date = '20250523'
# subfolder = r"2025-08-07_17-41-01_c5" # date = '20250516'
subfolder = r"2025-08-12_13-25-28_c5" # date = '20250717'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

cubic_int_dir = os.path.join(working_directory, 'cubic_interpolation_python')

roi_path = "NMF\\"+subfolder+"\\snr_selections"
roi_coord_dir = os.path.join(working_directory, roi_path)

#%%
def rms(data):
    """Calculate RMS"""
    return np.sqrt(np.mean(np.square(data)))

#%%
# LOADING ROI COORDINATES

# LOADING FILE NAMES
# # here I am just loading the names of the .txt files that contain the coordinates of the corners of the selection rectangle per ROI selected

files_coord = []

for item in os.listdir(roi_coord_dir):
    item_path = os.path.join(roi_coord_dir,item)
    
    if os.path.isfile(item_path) and item.endswith('.txt'):
        files_coord.append(item_path)
        
# RETRIEVEING COORDINATES PER FILE
# # here I am reading all the coordinates of the four corners of the selection rectangle per ROI selected in the image

coords_dic = {}

# read each line and make a list that contains a list per line
for i,path in enumerate(files_coord):    
    with open(path, 'r') as file:
        lines = [l.strip().split('\t') for l in file.readlines()] # read lines (.readlines()) and removes "\n" (.strip()) makes a list by removing "\t" (.split())
    
    # convert the coordinates into integers
    for l in range(1,len(lines)):
        for j in range(2):
            lines[l][j]=int(lines[l][j])
        
    coords_dic[i] = lines 
    
#%%    
# LOADING THE CUBIC INTERPOLATED IMAGES 
# # here I am loading all the cubic interpolated images corresponding to the ROI selected per ROI in coords_dic

roi_imgs = {}

# runs over the rois
for i in range(len(coords_dic)):
    
    # load the corresponding interpolated images
    fir_img_idx = coords_dic[i][1][1]
    last_img_idx = coords_dic[i][3][1]
    idx_array = np.arange(fir_img_idx, last_img_idx+1)
    
    temp_imgs = np.empty((len(idx_array),2048,2048), dtype=np.int32 )
    
    # runs over the image files amount of the selected roi
    for j,file in enumerate(idx_array):
        path = os.path.join(cubic_int_dir, f'image_{file:0{4}d}.npy')
        temp_imgs[j,:,:] = np.load(path)
    
    roi_imgs[f'ROI{i}'] = temp_imgs
    
#%%
# AVERAGE SPECTRUM CALCULATION
# # here I calculate the avg spectrum of the corresponding ROI for every ROI in roi_imgs

roi_avgs = {}

num_rois = len(roi_imgs)

# Runs over the ROIS
for i in range(num_rois):
    
    firs_row = coords_dic[i][1][0]
    last_row = coords_dic[i][2][0]
    idx_array = np.arange(firs_row, last_row+1)
    
    avg_per_img = []

    num_imgs = len(roi_imgs[f'ROI{i}'])
    
    # Runs over the images in the corresponding ROI
    for j in range(num_imgs):
        
        selection = roi_imgs[f'ROI{i}'][j][firs_row:last_row+1, :]
        avg_selec = np.mean(selection, axis=0)
        avg_per_img.append(avg_selec)
        
    avg_spec = np.mean(avg_per_img, axis=0)
    
    # avg_spec = (avg_spec - np.min(avg_spec)) /np.max(avg_spec) 
    
    roi_avgs[f'ROI{i}'] = avg_spec
    
#%%
# BASE LINE CORRECTION

baseline_specs = {}
background_specs = {}
noise = {}
baseline_obj = Baseline()

for i in range(num_rois):
    avg_spec = roi_avgs[f'ROI{i}']
    baseline_correction, params = baseline_obj.snip(avg_spec, max_half_window=10)
    baseline_corrected_spec = avg_spec - baseline_correction
    
    baseline_specs[f'ROI{i}'] = baseline_corrected_spec
                         
# Background substraction
    background_spec = avg_spec - baseline_corrected_spec
    background_specs[f'ROI{i}'] = background_spec
    
# NOISE CALCULATION
    noise[f'ROI{i}'] = rms(background_spec)
    

    

    
