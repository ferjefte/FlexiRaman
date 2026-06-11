# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 15:07:56 2025

Script to select a specific ROI in an interpolated set of images and save them 

@author: aguilafernando
"""

import numpy as np
import os 
import concurrent.futures
import time
from tqdm import tqdm
from pathlib import Path

# DIRECTORIES AND FOLDERS
project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")

date = '20250226'

sample = 'PS3_3'  
# sample = 'Si_F'

ROI = '01'

test = '01'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

#%%
# FUNCTION THAT SELECTS THE ROI AND SAVES THE NEW FILE

def roi_select(image_path, saving_folder, row_1, row_2, col_1, col_2):
    
    img = np.load(image_path)
    
    img_roi = img[row_1:row_2, col_1:col_2]
    
    save_name = os.path.join(saving_folder, image_path[-14:])
    
    np.save(save_name, img_roi)
    
# FUNCTION THAT MAKES THE PROCESS PARALLEL

def roi_parallel(working_directory, row_1, row_2, col_1, col_2):

    # FOLDER WITH THE INTERPOLATED MEASUREMENTS
    interp_folder = os.path.join(working_directory, "cubic_interpolation_python")

    with os.scandir(interp_folder) as entries:
        image_paths = [os.path.join(interp_folder, entry.name) for entry in entries ]
    image_paths.sort()
    print("image paths loaded")

    # FOLDER WHERE TO SAVE THE SELECTED ROI IMAGES
    interp_roi_folder = os.path.join(working_directory, "cubic_interpolation_roi_python")
    os.makedirs(interp_roi_folder, exist_ok=True)
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
          # Create a future for each file processing task
          futures = [
              executor.submit(roi_select, file, interp_roi_folder, row_1, row_2, col_1, col_2)
              for file in image_paths
          ]
          
          # Wait for all tasks to complete
          results = [f.result() for f in concurrent.futures.as_completed(futures)]
          
          success_count = sum(results)
    
    
    print(f"Processed {success_count}/{len(image_paths)} files successfully")
    end_time = time.time()
    print(f"time taken for roi extraction: {end_time-start_time/60}")

#%%

# # EXECUTION 

# if __name__ == "__main__":
        
#     roi_parallel(working_directory, 100, 600, 0, 2048)
    
 #%% NO PARALLEL 

# FOLDER WITH THE INTERPOLATED MEASUREMENTS
interp_folder = os.path.join(working_directory, "cubic_interpolation_python")

with os.scandir(interp_folder) as entries:
    image_paths = [os.path.join(interp_folder, entry.name) for entry in entries ]
image_paths.sort()
print("image paths loaded")

# FOLDER WHERE TO SAVE THE SELECTED ROI IMAGES
interp_roi_folder = os.path.join(working_directory, "cubic_interpolation_roi_python")
os.makedirs(interp_roi_folder, exist_ok=True)

start_time = time.time()
for file in tqdm(image_paths):
    roi_select(file, interp_roi_folder,  100, 600, 0, 2048)
end_time = time.time()

print(f"time taken for roi extraction: {end_time-start_time/60}")




