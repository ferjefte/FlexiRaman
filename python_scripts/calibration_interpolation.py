#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 14:36:28 2024

@author: fernandoaguila
"""

import numpy as np
import os
from interpolator_2 import (interpolator, grid_generator)
import logging 
from fnmatch import fnmatch
import tifffile as tiff
import time

# Configure logging
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

def contrast_gamma(img_in, min_in, max_in, min_out, max_out, gamma):
    try:
        img_clipped = np.clip((img_in.astype(np.float32) - min_in) / (max_in - min_in), 0, 1)
        return (img_clipped ** gamma) * (max_out - min_out) + min_out
    except Exception as e:
        print(f"Error in contrast_gamma: {e}")
        return None

def load_optimized_parameters(data_directory, order):
    param_path = os.path.join(data_directory, f'optimized_parameters_{order}_units.txt')
    try:
        with open(param_path, 'r') as file:
            opt_param_lines = file.readlines()
        opt_params = [float(line.split('\t')[1]) for line in opt_param_lines[:-2]]
        return opt_params
    except FileNotFoundError:
        print(f"Error: Parameter file not found at {param_path}")
        return None
    except ValueError as e:
        print(f"Error parsing parameter file {param_path}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading parameters: {e}")
        return None

def flexram_interp_calib(working_directory, data_directory, order, umethod, xi0_adj, yi0_adj, rot_adj, image_file_name = 'img_centermass.npy', slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668]):
    
    logger.info("Starting flexram_interp_calib function.")
    
    logger.info(f"Loading center mass numpy array from directory: {data_directory}")
    try:
        image_directory = os.path.join(working_directory, "calibration_data")
        image_name = np.load(os.path.join(image_directory, image_file_name))
        # mask_dialated = np.load(os.path.join(data_directory, f'mask_expand.npy'))
    except FileNotFoundError as e:
        print(f"Error loading image data: {e}")
        return
    except Exception as e:
        print(f"Unexpected error loading image data: {e}")
        return
    
    logger.info(f"Loading optimized parameters fron directory: {data_directory}")
    
    opt_params = load_optimized_parameters(data_directory, order)
    if opt_params is None:
        return
    
    Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6 = opt_params
    
    xi0 += xi0_adj 
    yi0 += yi0_adj
    rot += rot_adj
    
    test_points, fit_points = grid_generator(image_name, slit_dim_range, wavelen_range, 
                                             [Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6],
                                              data_directory, order)
    
    logger.info(f"{umethod} interpolating")
    
    try:
        im_s = np.array(interpolator(image_name, fit_points, test_points, umethod))
        im_s = im_s.reshape((2048,2048))
    except Exception as e:
        print(f"Error during interpolation: {e}")
        return
    
    # Saving results

    logger.info(f"saving {umethod} interpolated numpy array in {data_directory}")
    try:
        # NUMPY FILE
        im_s_directory = os.path.join(working_directory, f'{umethod}_interpolation_python')
        os.makedirs(im_s_directory, exist_ok=True)
        im_s_path = os.path.join(im_s_directory, 'image_0000.npy')
        np.save(im_s_path, im_s)
        # TIF FILE
        im_s_tif_directory = os.path.join(working_directory, 'interpolation_tif')
        os.makedirs(im_s_tif_directory, exist_ok=True)
        im_s_tif_path = os.path.join(im_s_tif_directory, f'calibration_image_{umethod}_interpolated.tif')
        tiff.imwrite(im_s_tif_path, im_s)

    except Exception as e:
        print(f"Error saving interpolation results: {e}")

    
    logger.info("Completed flexram_interp_calib function successfully.")


        
def flexram_interpolation_gpt(working_directory, dark_image_directory, 
                              data_directory,  
                               folder_name,  
                              order, umethod, 
                              file_ext='*.tif', 
                              y0i_adjust=0.174, rot_adjust=-0.1, xi0_adjust=0.2,  
                              n=2048, m=2048, 
                              slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668]):
    

        
        logger.info("Starting flexram_interpolation function.")
        
        # Check if directories exist
        if not os.path.isdir(working_directory):
            logger.error(f"Measured image directory '{working_directory}' not found.")
            raise FileNotFoundError(f"Measured image directory '{working_directory}' not found.")
        if not os.path.isdir(data_directory):
            logger.error(f"Data directory '{data_directory}' not found.")
            raise FileNotFoundError(f"Data directory '{data_directory}' not found.")
        
        # Change to the measured image directory and load image filenames
        logger.info(f"Accessing measured image directory: {working_directory}")
        with os.scandir(working_directory) as entries:
            image_content = [entry.name for entry in entries if fnmatch(entry.name, file_ext)]
        
        if not image_content:
            logger.error(f"No files matching '{file_ext}' found in directory '{working_directory}'.")
            raise FileNotFoundError(f"No files matching '{file_ext}' found in directory '{working_directory}'.")
            
        # Creating the folders to save the interpolation result
        new_folder = f'{order}_interpolation_python'
        full_path = os.path.join(working_directory, new_folder)
        # print(full_path)
        
        if not os.path.exists(full_path):
            os.mkdir(full_path)
            logger.info(f'New directory created in {full_path}')
        else:
            logger.info(f'Folder {new_folder} already exists')
    
        # Number of images
        l = len(image_content)
        logger.info(f"Found {l} images matching the file extension '{file_ext}'.")
        
        # Create an empty matrix to save all the measured images
        images = np.empty((n, m, l))
        
        # Read the measurement images and store them in the empty matrix
        for j, image_file in enumerate(image_content):
            try:
                image_path = os.path.join(working_directory, image_file)
                images[:, :, j] = tiff.imread(image_path)
                # logger.info(f"Successfully loaded image: {image_file}")
            except Exception as e:
                logger.error(f"Error loading image '{image_file}': {e}")
                raise IOError(f"Error loading image '{image_file}': {e}")
                
        images = np.int32(images)
        
        # Change to the data directory
        logger.info(f"Accessing data directory: {data_directory} for retrieving optimized parameter file")
        # os.chdir(data_directory)
        
        # Read optimized parameters from file with error checking
        param_file_name = f'optimized_parameters_{order}_units.npy'
        param_file_path = os.path.join(data_directory, param_file_name)
        if not os.path.isfile(param_file_path):
            logger.error(f"Parameter file '{param_file_name}' not found in directory '{data_directory}'.")
            raise FileNotFoundError(f"Parameter file '{param_file_name}' not found in directory '{data_directory}'.")
        
        try:
            opt_param = np.load(param_file_path)
            Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6 = opt_param
            logger.info("Successfully extracted parameters from the file.")
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing parameters from '{param_file_name}': {e}")
            raise ValueError(f"Error parsing parameters from '{param_file_name}': {e}")
        
        logger.info("Retrieving average dark image")
        # Read dark image average
        dark_image_path = os.path.join(dark_image_directory, 'avg_dark.npy')
        avg_darkimage = np.load(dark_image_path)
        avg_darkimage = np.int32(avg_darkimage)
        
        if not os.path.isfile(dark_image_path):
            logger.error(f"File '{dark_image_path}' not found")
            raise FileNotFoundError(f"File '{dark_image_path}' not found")
        
        # if not os.path.isfile(param_file):
        #     logger.error(f"Parameter file '{param_file}' not found in directory '{data_directory}'.")
        #     raise FileNotFoundError(f"Parameter file '{param_file}' not found in directory '{data_directory}'.")
    
        # try:
        #     with open(param_file, 'r') as r:
        #         opt_param_test = [line.split('\t') for line in r.readlines()]
        #     logger.info(f"Successfully read parameter file: {param_file}")
        # except Exception as e:
        #     logger.error(f"Error reading parameter file '{param_file}': {e}")
        #     raise IOError(f"Error reading parameter file '{param_file}': {e}")
        
        # Extract parameters
        # try:
        #     opt_param = [float(opt_param_test[i][1]) for i in range(len(opt_param_test) - 2)]
        #     Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6 = opt_param
        #     logger.info("Successfully extracted parameters from the file.")
        # except (ValueError, IndexError) as e:
        #     logger.error(f"Error parsing parameters from '{param_file}': {e}")
        #     raise ValueError(f"Error parsing parameters from '{param_file}': {e}")
        
        # Adjustments depending on the slit mask used   
        xi0 += xi0_adjust 
        yi0 += y0i_adjust
        rot += rot_adjust
        
        logger.info(f"Adjusted yi0 by {y0i_adjust}, new yi0: {yi0}")
        logger.info(f"Adjusted rot by {rot_adjust}, new yi0: {rot}")
        
        # Calculating grid data
        
        test_points, fit_points = grid_generator(images[:,:,0], slit_dim_range, wavelen_range, 
                                                  [Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6], data_directory)
        

        # Process each image
        for i in range(l):
            try:
                logger.info(f"Interpolating image {i+1}/{l}: {image_content[i]}")
                # Interpolation
                dark_corrected_image = images[:,:,i]-avg_darkimage
                dark_corrected_image[ dark_corrected_image<0 ]=0
                start_time = time.time()
                interpolated_image = interpolator(dark_corrected_image, fit_points, test_points, 
                                                            method=umethod)
                end_time = time.time()
                print(f"Time taken for cubic interpolation: {end_time - start_time:.6f} seconds")
                
            except Exception as e:
                logger.error(f"Error during interpolation for image '{image_content[i]}': {e}")
                raise RuntimeError(f"Error during interpolation for image '{image_content[i]}': {e}")
                
            # Saving the results
            file_name = f'image_{i+1}'
            file_path = os.path.join(full_path, file_name)
            np.save(file_path, interpolated_image)
            

        
        logger.info("Completed flexram_interpolation function successfully.")