# -*- coding: utf-8 -*-
"""
Created on Thu May 22 16:49:10 2025

@author: aguilafernando
"""

import numpy as np
import os
from interpolator_2 import (interpolator, grid_generator)
import logging 
from fnmatch import fnmatch
import tifffile as tiff
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from parameter_reader import parameter_reader, parameter_reader_slit
from pathlib import Path

# CONFIGURE LOGGING

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler('hyperspec_interpolation.log')
console_handler = logging.StreamHandler()

file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# FOLDER NAMES AND DIRECTORIES

project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")


# date = '20250717'
# date = '20250516'
# date = '20250408'
# date = '20260107'
date = '20260518'

# sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'
# sample = 'Volt'

ROI = '00'

test = '01'

slit = 'B1'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# DARK BACKGROUND AVERAGE FILE PATH

dark_directory = os.path.join(working_directory, 'dark')


### RETRIEVE VARIABLE FROM TEXT FILES ###################
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
slit_adj_path = os.path.join(data_directory, 'slit_adjustments.txt')

gen_param_dic = parameter_reader(general_parameters_path)
slit_adj_dic = parameter_reader_slit(slit_adj_path)

calib_slit_date = gen_param_dic['calib_slit_date']
order = gen_param_dic['order']
umethod = gen_param_dic['umethod']
file_ext = gen_param_dic['file_ext']

# IMAGE DIMENSIONS, SLIT RANGE AND WAVELENGTH RANGE
n = int(gen_param_dic['n'])
m = int(gen_param_dic['m'])
slit_dim_range = [float(gen_param_dic['slit_left']), float(gen_param_dic['slit_right'])]
wavelen_range = [int(gen_param_dic['wavelen_left']), int(gen_param_dic['wavelen_right'])]


yi0_adj = float(slit_adj_dic[slit][0])
rot_adj = float(slit_adj_dic[slit][1])
xi0_adj = float(slit_adj_dic[slit][2])

# CALIBRATION PARAMETERS FILE PATH
# calib_param_directory = os.path.join(project_directory, '20240906_Neon_lamp_test01', 'calibration_data') # old slit mask C4 (FR2022_4)
calib_param_directory = os.path.join(project_directory, '20260105_Neon_lamp_test01', 'calibration_data') # new slit mask B4 (FR2022_4)
calib_param_file_name = f'optimized_parameters_{order}_units.npy'
calib_param_file_path = os.path.join(calib_param_directory, calib_param_file_name)


#%%
def flexram_interpolation_gpt(working_directory, data_directory, dark_directory, calib_param_file_path, folder_name,
                              order, umethod, 
                              yi0_adj, rot_adj, xi0_adj, 
                              file_ext='*.tif',  n=2048, m=2048, 
                              slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668]):
    

        general_start = time.time()
        logger.info("Starting flexram_interpolation function.")
        
        # CHECKING IF DIRECTORIES EXIST
        
        measure_directory = os.path.join(working_directory, 'raw')
        if not os.path.isdir(measure_directory):
            logger.error(f"Measured image directory '{measure_directory}' not found.")
            raise FileNotFoundError(f"Measured image directory '{measure_directory}' not found.")
        if not os.path.isdir(data_directory):
            logger.error(f"Data directory '{data_directory}' not found.")
            raise FileNotFoundError(f"Data directory '{data_directory}' not found.")
            
        
        # LOADING IMAGE FILE'S NAMES
        
        logger.info(f"Accessing measured image directory: {measure_directory}")
        with os.scandir(measure_directory) as entries:
            image_content = [entry.name for entry in entries if fnmatch(entry.name, file_ext)]
        image_content.sort()
        
        if not image_content:
            logger.error(f"No files matching '{file_ext}' found in directory '{measure_directory}'.")
            raise FileNotFoundError(f"No files matching '{file_ext}' found in directory '{measure_directory}'.")
            
            
        # FOLDER CREATION FOR INTERPOLATION SAVING
        interpolations_path = os.path.join(working_directory, umethod+'_interpolation_python')
        
        if not os.path.exists(interpolations_path):
            os.mkdir(interpolations_path)
            logger.info(f'New directory created in {interpolations_path}')
        else:
            logger.info(f'Folder {interpolations_path} already exists')
            
        tif_file_folder = os.path.join(working_directory, 'interpolation_tif') 
        os.makedirs(tif_file_folder, exist_ok=True)
    
        # Number of images
        l = len(image_content)
        logger.info(f"Found {l} images matching the file extension '{file_ext}'.")
        
        
        # READ OPTIMIZED PARAMETERS
        
        logger.info(f"Accessing data directory: {data_directory} for retrieving optimized parameter file")
        
        if not os.path.isfile(calib_param_file_path):
            logger.error(f"Parameter file '{calib_param_file_name}' not found in directory '{data_directory}'.")
            raise FileNotFoundError(f"Parameter file '{calib_param_file_name}' not found in directory '{data_directory}'.")
        
        try:
            opt_param = np.load(calib_param_file_path)
            Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6 = opt_param
            logger.info("Successfully extracted parameters from the file.")
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing parameters from '{calib_param_file_name}': {e}")
            raise ValueError(f"Error parsing parameters from '{calib_param_file_name}': {e}")
        
        
        # READ DARK IMAGE AVERAGE 
        
        logger.info("Retrieving average dark image")
        
        dark_image_path = os.path.join(dark_directory, 'avg_dark.npy')
        avg_darkimage = np.load(dark_image_path)
        avg_darkimage = np.float32(avg_darkimage)
        
        if not os.path.isfile(dark_image_path):
            logger.error(f"File '{dark_image_path}' not found")
            raise FileNotFoundError(f"File '{dark_image_path}' not found")
            
        
        # ADJUSTMENTS DUE TO SLIT MASK USED
        
        logger.info(f"Old xi0 : {xi0}")
        logger.info(f"Old yi0 : {yi0}")
        logger.info(f"Old rot : {rot}")
        
        xi0 += xi0_adj 
        yi0 += yi0_adj
        rot += rot_adj
        
        logger.info(f"Adjusted xi0 by {xi0_adj}, new xi0: {xi0}")
        logger.info(f"Adjusted yi0 by {yi0_adj}, new yi0: {yi0}")
        logger.info(f"Adjusted rot by {rot_adj}, new rot: {rot}")
        
        
        # # LOADING GAUSS CORRECTION MATRIX (in case nothing in setup was moved) (gauss calibration corresponidng to measurements on 20250226 B5 PS3 test01)
        
        # gauss_matrix_path = os.path.join(data_directory, gauss_correction_name)
        # gauss_matrix = np.load(gauss_matrix_path)
        
        
        # CALCULATING GRID DATA
        
        image_path_0 = os.path.join(measure_directory, image_content[0])
        image_0 = tiff.imread(image_path_0)
        
        test_points, fit_points = grid_generator(image_0, slit_dim_range, wavelen_range, 
                                                  [Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6], data_directory)
        
        
        # IMAGE DIVISION INTO CHUNKS FOR PARALLELIZATION
        
        # dividing the images in chunks to parallelize and accelerate the interpolation
        tp_r = len(test_points)
        # print(f'len test_points: {tp_r}')
        chunk_size = int(tp_r/2)
        # print(f'chunk_size: {chunk_size}')
        test_points_chunks = [ test_points[i:i+chunk_size] for i in range(0,tp_r,chunk_size) ]
        
        
        # INTERPOLATION PROCESS FOR EACH IMAGE
        
        for i,image_file in enumerate(image_content):
            try:
                image_path = os.path.join(measure_directory, image_file)
                image = tiff.imread(image_path)
                # logger.info(f"Successfully loaded image: {image_file}")
            except Exception as e:
                logger.error(f"Error loading image '{image_file}': {e}")
                raise IOError(f"Error loading image '{image_file}': {e}")
                
            image = np.float32(image)
            
            logger.info(f"Interpolating image {i+1}/{l}") #{image_content[i]}
            try:
                # DARK CORRECTION 
                
                dark_corrected_image = image-avg_darkimage
                # dark_corrected_image = image
                dark_corrected_image[ dark_corrected_image<0 ]=0
                
                interpolated_image = []
                
                # INTERPOLATION
                
                start_time = time.time()
                
                with ProcessPoolExecutor() as executor :
                    future_to_chunk = { executor.submit( interpolator, dark_corrected_image, fit_points, chunk): chunk for chunk in test_points_chunks  }
                    for future in as_completed(future_to_chunk):
                        interpolated_image.extend(future.result())
                
                interpolated_image = np.array(interpolated_image).reshape(n,m)
                
                end_time = time.time()
                print(f"Time taken for cubic interpolation: {end_time - start_time:.6f} seconds")
            
            except Exception as e:
                logger.error(f"Error during interpolation for image '{image_content[i]}': {e}")
                raise RuntimeError(f"Error during interpolation for image '{image_content[i]}': {e}")
                
                
            # GAUSS CORRECTION
            
            # interpolated_image = interpolated_image/gauss_matrix   
            
            
            # SAVING RESULT 
            
            number_str = f"{i:0{4}d}"
            file_name = f"image_{number_str}"
            file_path = os.path.join(interpolations_path, file_name)
            np.save(file_path, interpolated_image)
            
            tif_image = np.array(interpolated_image, dtype=np.float32)
            tif_image_path = os.path.join(tif_file_folder, f"image_{number_str}.tif")
            tiff.imwrite( tif_image_path, tif_image,
                              imagej=True, resolution=(1/0.000234,1/0.000234), metadata={'spacing': 0.000234, 'unit': 'mm', 'axes': 'YX', 'mode': 'grayscale'}
                             )
        

        general_end = time.time()
        print(f"Time for interpolation: {(general_end-general_start)/60}")
        logger.info("Completed flexram_interpolation function successfully.")

#%%
# FUNCTION RUNNING 

if __name__ == '__main__':
    flexram_interpolation_gpt(working_directory, data_directory, dark_directory, calib_param_file_path, folder_name,
                              order, umethod, 
                              yi0_adj, rot_adj, xi0_adj,
                              file_ext, 
                              n, m, 
                              slit_dim_range, 
                              wavelen_range)