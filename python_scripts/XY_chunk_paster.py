# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 16:34:49 2025

@author: aguilafernando
"""

# PROGRAM TO PASTE ALL THE CHUNKS OF THE RESLICED INTERPOLATED IMAGES

import os 
import numpy as np
import time
from tqdm import tqdm
import tifffile
from parameter_reader import parameter_reader


#%%

# DIRECTORIES AND PATHS

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'
calib_param_directory = os.path.join(project_directory, '20240906_Neon_lamp_test01\\calibration_data')
gauss_correction_name = 'vertical_gauss_correction_matrix_20250408.npy'

# date = '20250516'
date = '20250717'
# date = '20250408'

sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
# sample = 'Pig01_C'
# sample = 'Volt'

ROI = '03'

test = '02'

chunks = 5

# GENERAL PARAMETERS
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
gen_param_dic = parameter_reader(general_parameters_path)

# WORKING DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# INTERPOLATIONS DIRECTORY
umethod = gen_param_dic['umethod']
interpolations_directory = os.path.join(working_directory, umethod+'_interpolation_python')



reslice_img_chunks_path = os.path.join(working_directory, 'XY_chunks')
reslice_img_path = os.path.join(working_directory, 'XY_python')
reslice_img_tif_path = os.path.join(working_directory, 'XY_tif')

# Create output directories
os.makedirs(reslice_img_path, exist_ok=True)
os.makedirs(reslice_img_tif_path, exist_ok=True)
#%%

# LOADING IMPORTANT DATA

# Wavelengths
wavelen_path = os.path.join(calib_param_directory, 'wavelengths.npy')
wavelen = np.load(wavelen_path)
wavelen_shift = 1e7/532 - (1e7/wavelen)


#%%

def stack_chunks(reslice_chunks_folder, wavelen_idx, number_chunks):
    wavelen_strg = round(wavelen_shift[wavelen_idx],2)
    
    chunks_load = [
        np.load( os.path.join(reslice_chunks_folder, f"resliced_image_{wavelen_strg}_chunk{i:0{2}d}.npy") )
        for i in np.linspace(1,number_chunks, number_chunks, dtype=int)
        ]
        
    whole_img = np.hstack(chunks_load)
    whole_img = whole_img.T
    n, m = np.shape(whole_img)
    h_g_m = np.load( os.path.join(data_directory, gauss_correction_name) )
    j, k = np.shape(h_g_m)
    
    if n>j:
        k = n-m
        last_row = h_g_m[-1:]
        new_rows = np.tile(last_row, (k,1))
        h_g_m = np.vstack((h_g_m, new_rows))
        
    # whole_img_gc = whole_img/h_g_m[0:n, :]
    whole_img_gc = whole_img
    whole_img_tif = np.array(whole_img_gc, dtype=np.uint16)
    # whole_img_tif = whole_img_tif.T
    
    
    np.save( os.path.join(reslice_img_path, f"{wavelen_idx:0{4}d}_resliced_image_"+sample+"_test"+test+f"_{wavelen_strg}.npy"), whole_img)
    tifffile.imwrite( os.path.join(reslice_img_tif_path, f"{wavelen_idx:0{4}d}_resliced_image_"+sample+"_test"+test+f"_wavenum_{wavelen_strg}.tif"),
                     whole_img_tif, imagej=True, resolution=(1/0.000234,1/0.000234), metadata={'spacing': 0.000234, 'unit': 'mm', 'axes': 'YX', 'mode': 'grayscale'}
                     )


#%%
# PASTING CHUNKS AND CREATING tif IMAGE FILES

start_time = time.time()
print("Stacking chunks vertically..")

for wave_idx, wave in tqdm(enumerate(wavelen_shift)):
    stack_chunks(reslice_img_chunks_path, wave_idx, chunks)

end_time = time.time()
print(f"\nMinutes for reslicing: {(end_time-start_time)/60}")
