# -*- coding: utf-8 -*-
"""
Created on Tue May 27 16:05:13 2025

FUNCTION TO LOAD THE CALIBRATION RAW IMAGES AND AVERAGE THEM

@author: aguilafernando
"""

import numpy as np
import os
# import scipy.ndimage as ndimage
import logging 
from function_collection import read_measurements_pbirms
from fnmatch import fnmatch
import tifffile as tiff

# CONFIGURE LOGGING

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler('image_loader.log')
console_handler = logging.StreamHandler()

file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def img_load_avg(working_directory):
    
    # DIRECTORY FOR SAVING DATA
    data_directory = os.path.join(working_directory, 'calibration_data')
    os.makedirs(data_directory, exist_ok=True)
    
    img_hi_nof=read_measurements_pbirms(working_directory+'\\no_filter')['avg_imgs']
    np.save(data_directory+'\\img_hi_nof', img_hi_nof)


    img_hi_dark_nof=read_measurements_pbirms(working_directory+'\\no_filter\\dark')['avg_imgs']
    np.save(data_directory+'\\img_hi_dark_nof', img_hi_dark_nof)

    img_hi_yesf=read_measurements_pbirms(working_directory+'\\filter')['avg_imgs']
    np.save(data_directory+'\\img_hi_yesf', img_hi_yesf)

    img_hi_dark_yesf=read_measurements_pbirms(working_directory+'\\filter\\dark')['avg_imgs']
    np.save(data_directory+'\\img_hi_dark_yesf', img_hi_dark_yesf)

    # # CASE when the green filter and the band pass filter are used at the same time

    # img_hi_yesf_g=read_measurements_pbirms(working_directory+'\\filter_gfilter')['avg_imgs']
    # np.save(data_directory+'\\img_hi_yesf_g', img_hi_yesf_g)

    # img_hi_dark_yesf_g=read_measurements_pbirms(working_directory+'\\filter_gfilter\\dark')['avg_imgs']
    # np.save(data_directory+'\\img_hi_dark_yesf_g', img_hi_dark_yesf_g)
    
def background_average(darkimage_directory, file_ext='*.tif'):
    
    logger.info(f'Retrieving dark image from directory: {darkimage_directory}')
    
    
    with os.scandir(darkimage_directory) as entries:
        dark_images_names = [entry.name for entry in entries if fnmatch(entry.name, file_ext)]
    
    if not darkimage_directory:
        logger.error(f"Directory: '{darkimage_directory}' not found")
        raise FileNotFoundError(f"Directory: '{darkimage_directory}' not found")
        
    # create empty matrix array to save the dark images
    dark_images = []
        
    for image_name in dark_images_names:
        try:
            image_path = os.path.join(darkimage_directory, image_name)
            image = tiff.imread(image_path)
            image = np.float32(image)
            dark_images.append(image)
            
        except Exception as e:
            logger.error(f"Error loading image: '{image_path}': {e}")
            raise IOError(f"Error loading image: '{image_path}': {e}")
            
    dark_images = np.array(dark_images)
    
    # Averaging the dark images
    logger.info("Calculating average")
    stacked_dark_images = np.stack(dark_images)
    avg_darkimage = np.mean(stacked_dark_images, axis=0)
    # print(np.shape(avg_darkimage))
    
    # Saving average
    logger.info(f"Average of dark images saved in: '{darkimage_directory}'")
    avg_darkimage_path = os.path.join(darkimage_directory, 'avg_dark.npy')
    np.save(avg_darkimage_path, avg_darkimage)
    