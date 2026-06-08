# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 15:55:42 2025

SCRIPT TO CALCULATE THE GAUSSIAN PARAMETERS OF AN IMAGE FOR LATER GAUSSIAN VIGNETING ADJUSTMENT

THE DESIRED IMAGE TO CORRECT HAS TO BE LOADED
THEN A Z PRJECTION IS MADE FOR THE GAUSSIAN GAUSSIAN FITTING
THE GAUSSIAN PARAMETERS (AMPLITUDE, MU, SIGMA) ARE CALCULATED AND SAVE TO A "opt_gauss_param_{date}_{sample}.txt" FILE

@author: aguilafernando
"""


import os
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#%%
# CORRESPONDING FOLDER AND IMAGE NAMES

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

# date = '20250408'
# date = '20250717'
# date = '20250523'
# date = '20250516'
date = '20260107'

sample = 'PS3_3'  
# sample = 'Si_F'
# sample = 'Pig01_C'

# ROI = '02'
ROI = '01'
# ROI = '03'

test = '01'

# subfolder = r"2026-01-13_13-54-50_c5" # date = '20250523' fuve
# subfolder = r"2026-01-14_18-29-29_c7" # date = '20250523' seven
# subfolder = r"2026-01-13_14-31-09_c5" # date = '20250516' five
# subfolder = r"2026-01-14_18-36-19_c7" # date = '20250516' seven
# subfolder = r"2026-01-15_11-36-33_c5" # date = '20250717' five
# subfolder = r"2026-01-14_17-01-26_c7" # date = '20250717' seven
# subfolder = r"2026-01-13_12-00-38_c3" # date = '20260107' three 
# subfolder = r"2026-01-13_11-12-08_c5" # date = '20260107' five 
# subfolder = r"2026-01-15_18-52-56_c7" # date = '20260107' seven NMF
subfolder = r"2026-04-27_14-59-07_c7" # date = '20260107' seven # corrected for horizontal shift 
# subfolder = r"2026-01-14_18-48-46_c7" # date = '20260107' seven PCA

# jj = 184
# jj = 0
jj = 169 # date = '20260107' seven

case_ = 'NMF'
# case_ = 'PCA'

# wavenum = ['519.75', '0114']

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# CALCULATE THE GAUSSIAN PARAMETERS FOR EACH IMAGE

i_imgs = 7

for i in range(i_imgs):

    # # RESLICE IMAGE
    # reslice_folder_path = os.path.join(working_directory, 'XY_python')
    # reslice_image_path = os.path.join(reslice_folder_path, wavenum[1]+'_resliced_image_'+sample+'_'+'test'+test+'_'+wavenum[0]+'.npy')
    if case_ == 'NMF':
        # IMAGE PATH
        reslice_folder_path = os.path.join(working_directory, "NMF\\"+subfolder+"\\W_jj"+ str(jj).zfill(5))
        image_name = "W_" + str(i).zfill(5) + ".tif"
        reslice_image_path = os.path.join(reslice_folder_path, image_name)
    
    if case_ == 'PCA':
        # PCA CASE
        reslice_folder_path = os.path.join(working_directory, "PCA\\"+subfolder+"\\W")
        image_name = "W_" + str(0).zfill(5) + ".tif"
        # image_name = "W_" + str(i).zfill(5) + ".tif" # case where parameters are calculated for each image
        reslice_image_path = os.path.join(reslice_folder_path, image_name)
    
    
    #%%
    # GAUSSIAN DEFINITION
    
    def gaussian(x, A, mu, sigma):
        return A * np.exp(-(x - mu)**2 / (2 * sigma**2))
    
    #%%
    # IMAGE SELECTION
    image_tiff = tf.TiffFile(reslice_image_path)
    image = image_tiff.pages[0].asarray() # rgb image (n,m,3)
    
    # selecting the NMF-component for the Gaussian parameter calculation
    
    # # case date = '20250717'
    # image = image[:,:,1]
    
    # # case date = '20250523'
    # image = image[:,:,2]
    
    # # case date = '20250516'
    # image = image[:,:,2]
    
    # case date = '20260107'
    rgb_img = image
    
    # image = np.load(reslice_image_path) 
    # image = image.T
    
    n, m = np.shape(image)
    
    fig, axes = plt.subplots(1,1)
    axes.imshow(image)
    
    #%%
    # Z-PROJECT
    
    z_collapsed_image = np.sum(image, axis=0)
    
    # array with pixels indices 
    x = np.linspace(0,m,m)
    
    #%%
    # GAUSSIAN FITTING 
    
    popt_g, pcov_g = curve_fit(gaussian, x, z_collapsed_image, p0=[1,1,1]) 
    
    
    # Extract the fitted parameters
    A_fit_green, mu_fit_green, sigma_fit_green = popt_g
    
    print(f"Fitted parameters: A={A_fit_green}, mu={mu_fit_green}, sigma={sigma_fit_green}")
    
    
    # Saving parameters order: 1) GREEN PARAMETERS, 2) RED PARAMETERS 
    
    # RESLICE IMAGE
    saving_directory = os.path.join(working_directory, "gauss_correction_param")
    os.makedirs(saving_directory, exist_ok=True)
    
    gauss_params_file_path = os.path.join(saving_directory, f'opt_gauss_param_{i}_{case_}_{date}_{sample}.txt')
    
    # order of saving = [amp_green, mu_green, sigma_green, amp_red, mu_red, sigma_red] in pixel units
    
    with open(gauss_params_file_path, 'w') as f:
        f.write(f"Amplitude\t{A_fit_green}\n")
        f.write(f"mu\t{mu_fit_green}\n")
        f.write(f"sigma\t{sigma_fit_green}\n")
    
    
    # Generate the fitted curve
    y_fit_g = gaussian(x, A_fit_green, mu_fit_green, sigma_fit_green)
    
    
    
    #%%
    # PLOTTING 
    
    fig, axes = plt.subplots(1,1)
    
    # RESLICE IMAGE
    axes.plot(z_collapsed_image)
    
    axes.plot(x, y_fit_g)
    
