# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 14:13:42 2025

# RESLICE OF INTERPOLATED IMAGES BY CHUNKS 

@author: aguilaremote
"""


import os 
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
import gc
import shutil
from parameter_reader import parameter_reader
from tqdm import tqdm

#%%
# FOLDER CONTENTS ERASER 

def erase_folder_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            
# # DIVISION INDEXES ARRAY

# def create_500_step_array(number_images, chunk_size):
#     steps = n // chunk_size
#     if n % chunk_size != 0:
#         steps += 1
#     array = np.linspace(0, n, num=steps+1, dtype=int)
#     return array, len(array)

# FUNCTION TO DIVIDE THE INTERPOLATED FILES INTO CHUNKS AND THEN MOVE THEM TO SEPARATE FOLDERS

def images_divider(interp_dic, batch_size):
    # Retrieve names of files
    files = os.listdir(interp_dic)
    l = len(files)
    num_chunks = l//batch_size +1
    # count = 1
    
    # Divide the files in batches and create a folder for each batch
    for i in range(0,l,batch_size):
        batch = files[i:i+batch_size]
        part = i//batch_size + 1
        batch_dir = interp_dic+f'_part{part:0{2}d}'
        os.makedirs(batch_dir, exist_ok=True)
        
    # while l!=0:
    #     batch = files[0:batch_size+1]
    #     batch_dir = interp_dic+f'_part{count:0{2}d}'
    #     os.makedirs(batch_dir, exist_ok=True)
        
        # Move the batch to the corerspoding folder
        for file in tqdm(batch):
            file_path = os.path.join(interp_dic, file)
            file_dest_path = os.path.join(batch_dir, file)
            shutil.copy2(file_path, file_dest_path)
           
        # count = count + 1 
        # files = os.listdir(interp_dic)
        # l = len(files)
        
    return num_chunks

# FUNCTION TO PERFORM RESLICING AND THREADING

def process_images(file_paths, output_dir, trash_dir, iterator, n, m):
    image_shape = (n, m)   # Assuming each image is 2048x2048
    
   # Create temp arrays to save resliced images         
    output_arrays = [ 
                      np.memmap(  os.path.join( trash_dir, f"resliced_image_{round(wavelen_shift[col_idx],2)}.temp.npy" ),
                          dtype=np.float32, mode="w+", shape=(n,l) 
                                )
                      for col_idx in range(image_shape[1])   
                     ]
    
    # Function to perform reslicing
    def load_and_extract_columns(file_path, file_idx):
        img = np.load(file_path)  # Shape: (2048, 2048) loads one original (interpolated) image
        for col_idx in range(image_shape[1]): # scans over the columns of img and each resliced image 
                output_arrays[col_idx][:, file_idx] = img[:, col_idx]  # Extract column
        # output_arrays.flush()
        
    # Parallelize I/O and column extraction
    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust workers for disk I/O
      executor.map(lambda x: load_and_extract_columns(x[1], x[0]), enumerate(file_paths) ) 
    gc.collect() # close any threads left open
    
    # Save all output images
    for col_idx, arr in enumerate(output_arrays):
        resliced_image_path = os.path.join(output_dir, f"resliced_image_{round(wavelen_shift[col_idx],2)}_chunk{iterator:0{2}d}.npy")
        np.save(resliced_image_path, arr)
        
#%%

# DIRECTORIES AND PATHS

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'
calib_param_directory = os.path.join(project_directory, '20240906_Neon_lamp_test01\\calibration_data')

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

# GENERAL PARAMETERS
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
gen_param_dic = parameter_reader(general_parameters_path)

# WORKING DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

#%%
# DIVIDING INTERPLATED IMAGES IN BATCHES AND SAVING THEM IN SEPARATE FOLDERS

# INTERPOLATIONS DIRECTORY
umethod = gen_param_dic['umethod']
interpolations_directory = os.path.join(working_directory, umethod+'_interpolation_python')

print('Copying files and dividing in chunks...')
start_time_c = time.time()
chunks = images_divider(interpolations_directory, 500) 
end_time_c = time.time()
print(f"\nMinutes for copying and dividing: {(end_time_c-start_time_c)/60}")

#%%

for i in np.linspace(1,chunks,chunks, endpoint=True, dtype=int ):
    
    chunk_interp_directory = interpolations_directory+f'_part{i:0{2}d}'

    reslice_img_chunks_path = os.path.join(working_directory, 'XY_chunks')
    trash_dir =  os.path.join(working_directory,'trash')
    
    # Create output directory
    os.makedirs(reslice_img_chunks_path, exist_ok=True)
    os.makedirs(trash_dir, exist_ok=True)
    
    # Erase trash folder
    erase_folder_contents(trash_dir)
    

    
    # LOADING IMPORTANT DATA
    
    # Wavelengths
    wavelen_path = os.path.join(calib_param_directory, 'wavelengths.npy')
    wavelen = np.load(wavelen_path)
    wavelen_shift = 1e7/532 - (1e7/wavelen)
    

    # LOADING FIRST IMAGE
    
    # List all .npy files in the directory
    image_files = [f for f in os.listdir(chunk_interp_directory) if f.endswith('.npy')]
    image_files.sort()
    l = len(image_files)  # Number of images
    
    # Load the first image to get dimensions n and m
    first_image = np.load( os.path.join(chunk_interp_directory, image_files[0]) )
    n, m = first_image.shape  # Assuming all images have the same dimensions
    

    # Reslicing
    start_time = time.time()
     
    ## with partition image files
    # divisions, len_divisions = create_500_step_array(l, 500)
    
    # for k in tqdm(range(len(divisions)-1)):
    #         indices = [i for i in np.arange(divisions[k], divisions[k+1], 1, dtype=int) ]
    #         file_paths = [ os.path.join(interpolations_directory, image_files[i])
    #                       for i in np.arange(divisions[k], divisions[k+1], 1, dtype=int)
    #                    ]
    #         print(len(file_paths))
    #         process_images(file_paths, reslice_img_chunks_path, trash_dir)
    
    ## without partition of image files
    file_paths = [ os.path.join(chunk_interp_directory, image_files[i]) 
                  for i in range(l) ]
    # print(len(file_paths))
    print("Reslicing...")
    process_images(file_paths, reslice_img_chunks_path, trash_dir, i, n, m)
    
    end_time = time.time()
    print(f"Minutes for reslicing: {(end_time-start_time)/60}")




