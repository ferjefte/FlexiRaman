# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 14:03:52 2025

# SCRIPT TO OBTAIN THE GAUSSIAN VIGNETING CORRECTION MATRIX

GAUSSIAN FUNCTION DEFINITION IS NOT TAKING AMPLITUDE INTO ACCOUNT

IMAGE TO BE CORRECTED AND FROM WHICH THE GAUSSIAN PARAMETERS WERE CALCULATED IS USED
NMF-COMPONENT-IMAGE CHANGES WITH THE SAMPLE

GAUSSIAN PARAMETERS ARE LOADED AND THEN THE GAUSSIAN CORRECTION MATRIX IS MADE AND SAVED

THE VERTICAL CASE IS ALSO CALCULATED BUT UNUSED. ONLY HORIZONTAL CASE IS USED


@author: aguilaremote
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import tifffile as tf
import cv2

#%%
# GAUSS FUNCTION DEFINITION 

def gauss(sigma, mu, amp, x):
    # y = amp  * np.exp( -( x - mu )**2/( 2*sigma**2 ) )  # with amp
    y = np.exp( -( x - mu )**2/( 2*sigma**2 ) )
    # norm = np.exp( -( x - mu )**2/( 2*sigma**2 ) )
    
    # fig, ax = plt.subplots(1,1)
    # ax.plot(x,y)
    
    return y

#%%
# DIRECTORIES AND FOLDERS

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

# PCA
# jj = 184
# jj = 6

# GAUSS VIGNETING CORRECTION CONSIDERING INDIVIDUAL PARAMETERS FOR EVERY IMAGE

i_imgs = 7 

for i in range(i_imgs):
    
    # NMF
    jj = 169 # date = '20260107' seven 
    ii = i
    
    case_ = 'NMF'
    # case_ = 'PCA'
    
    # wavenum = ['519.75', '0114']
    
    # RAW MEASUREMENTS DIRECTORY
    folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
    working_directory = os.path.join(project_directory, folder_name)
    
    
    # # RESLICE IMAGE
    # reslice_folder_path = os.path.join(working_directory, 'XY_python')
    # reslice_image_path = os.path.join(reslice_folder_path, wavenum[1]+'_resliced_image_'+sample+'_'+'test'+test+'_'+wavenum[0]+'.npy')
    
    # # IMAGE PATH
    # reslice_folder_path = os.path.join(working_directory, "NMF\\"+subfolder)
    # image_name = "W_RGBjj" + str(jj).zfill(5) + ".tiff"
    # reslice_image_path = os.path.join(reslice_folder_path, image_name)
    
    if case_ == 'NMF':
        # IMAGE PATH
        reslice_folder_path = os.path.join(working_directory, "NMF\\"+subfolder+"\\W_jj"+ str(jj).zfill(5))
        image_name = "W_" + str(ii).zfill(5) + ".tif"
        reslice_image_path = os.path.join(reslice_folder_path, image_name)
    
    if case_ == 'PCA':
        # PCA CASE
        reslice_folder_path = os.path.join(working_directory, "PCA\\"+subfolder+"\\W")
        image_name = "W_" + str(i).zfill(5) + ".tif"
        reslice_image_path = os.path.join(reslice_folder_path, image_name)
    
    #%%
    
    # IMAGE LOADING
    
    image_tiff = tf.TiffFile(reslice_image_path)
    image = image_tiff.pages[0].asarray() # rgb image (n,m,3)
    
    # # case date = '20250523'
    # rgb_img = image[:,:,2]
    
    # # case date = '20250516'
    # rgb_img = image[:,:,2]
    
    # # case date = '20250717'
    # rgb_img = image[0:2048,:,0]
    
    # # single image case
    # rgb_img = np.load(reslice_image_path)
    # rgb_img = rgb_img
    
    # case date = '20260107'
    rgb_img = image
    
    n,m = np.shape(rgb_img)
    
    # GRID
    grid = np.linspace(0,m,m)
        
    #%%    
    # GAUSSIAN PARAMETERS LOADING
    saving_directory = os.path.join(working_directory, "gauss_correction_param")
    gauss_params_file_path = os.path.join(saving_directory, f'opt_gauss_param_{i}_{case_}_{date}_{sample}.txt')
    
    with open(gauss_params_file_path, 'r') as f:
        lines = f.readlines()
        
    param_array = []
        
    for l in lines:
        u,v = l.strip().split('\t')
        param_array.append(float(v))
        
    # PARAMETES FOR GREEN AND BLUE CHANNELS
    # CENTERGAUSS IS THE CENTER PIXEL FOR THE VIGNETTING 
    # SIGM IS THE VARIANCE OF THE GAUSS SHAPED VIGNETTING IN X DIRECTION 
    
    # RESLICE IMAGE
    ampli_g, centerGauss_g, sigm_g = param_array
    
    
    #%%
    # CALCULATIONS
    
    #green
    y_g = gauss(sigm_g, centerGauss_g, ampli_g, grid) 
    
    # reshape y_g from (m,) to (m,1) (vertical case)
    y_g_v = y_g.reshape((m,1))
    
    # reshape y_g from (m,) to (1,m) (horizontal case)
    y_g_h = y_g.reshape((1,m))
    
    # print(np.max(rgb_img[:,:]))
    # print(np.min(rgb_img[:,:]))
    
    # GAUSSIAN VIGNETING CORRECTION MATRIXES
    # Matrix for interpolation correction (vertical orientation)
    g_m_v = np.full((m,n), y_g_v, dtype=np.float64)
    
    # Matrix for reslicing correction (horizontal orientation)
    g_m_h =  np.full((n,m), y_g_h, dtype=np.float64)
    
    
    # CORRECTION 
    
    g_c_green = rgb_img[:,:]/g_m_v.T
    g_c_green2 = rgb_img[:,:]/g_m_h
    
    # saving green gaussian corrected image
    # v_g_m = os.path.join(data_directory, 'vertical_gauss_correction_matrix_'+sample+'_'+date+'.npy')
    # np.save(v_g_m, g_m_v)
    
    # h_g_m = os.path.join(data_directory, 'horizontal_gauss_correction_matrix_'+sample+'_'+date+'.npy')
    # np.save(h_g_m, g_m_h)
    
    
    # PLOT COMPARISON
    
    fig, ax = plt.subplots(2,3)
    ax[0,0].imshow(rgb_img)
    ax[0,1].imshow(g_m_v)
    ax[0,2].imshow(g_c_green)
    
    ax[1,0].imshow(rgb_img)
    ax[1,1].imshow(g_m_h)
    ax[1,2].imshow(g_c_green2)
    
    
    # gaussvignettign = 1/np.sqrt(2*np.pi*sigm**2)*np.exp(-(grid-centerGauss)**2/(2*sigm**2)) #not what we want actually
    # normgaussvignettign = np.exp(-(grid-1000)**2/(2*sigm**2))
    
    # SAVING
    Bittype=np.float32
    
    gauss_tif_folder = reslice_folder_path + "_gauss"
    os.makedirs(gauss_tif_folder, exist_ok=True)
    
    gauss_corr_img_path = os.path.join(gauss_tif_folder, "W_" + str(ii).zfill(5) + ".tiff")
    tf.imwrite(gauss_corr_img_path, g_c_green.astype(Bittype), imagej=True, resolution=(1/0.234, 1/0.234)) 
    
    
    
    
    
