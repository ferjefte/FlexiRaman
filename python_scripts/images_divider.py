# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:33:18 2025

@author: aguilafernando
"""
import os
import shutil
from tqdm import tqdm

#%%
# FUNCTION THAT MAKES COPIES AND DIVIDES THE TOTAL IMAGES AMOUNT IN FOLDERS OF "BATCH SIZE" IMAGES

def images_divider(interp_dic, batch_size):
    # Retrieve names of files
    files = os.listdir(interp_dic)
    l = len(files)

    
    # Divide the files in batches and create a folder for each batch
    for i in range(0,l,batch_size):
        batch = files[i:i+batch_size]
        part = i//batch_size + 1
        batch_dir = interp_dic+f'_part{part:0{2}d}'
        os.makedirs(batch_dir, exist_ok=True)
        
        
        # Move the batch to the corerspoding folder
        for file in tqdm(batch):
            file_path = os.path.join(interp_dic, file)
            file_dest_path = os.path.join(batch_dir, file)
            shutil.copy2(file_path, file_dest_path)
           
#%%

# DIRECTORY

project_directory = r'D:\Projekte\Flexiraman\Fernando'

date = '20250516'
# date = '20250514'

# sample = 'PS3_P'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'

ROI = '02'

test = '01'

# WORKING DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

img_directory = os.path.join(working_directory, 'interpolation_tif')

images_divider(img_directory, 500)