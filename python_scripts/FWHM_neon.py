# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 15:25:13 2025

@author: aguilafernando
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path

#%%

# FOLDER NAMES AND DIRECTORIES
project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")

date = '20251029'
date = '20240906'
date = '20260106'

sample = 'Neon_lamp'

test = '01'

# DIRECTORY
folder_name =  date+'_'+sample+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

cubic_int_dir = os.path.join(working_directory, 'cubic_interpolation_python')
calib_data_dir = os.path.join(working_directory, "calibration_data")

# file name changes according to the measurement. C4 slit measurements -> img_centermass.npy. B5 slit measurements -> image_0000.npy
cubic_int_file_path = os.path.join(cubic_int_dir, 'image_0000.npy')

xi_file_path = os.path.join(calib_data_dir, 'xi.npy')
wavelens_file_path = os.path.join(calib_data_dir, 'wavelengths.npy')


#%%
# LOADING
cubic_int = np.load(cubic_int_file_path)

xi = np.load(xi_file_path)
wavelens = np.load(wavelens_file_path)
wavelens = wavelens.flatten()

#%%
# PROCESSING
min_val = np.min(cubic_int)
max_val = np.max(cubic_int) 

cubic_int[cubic_int<0] = 0

min_val_adj = np.min(cubic_int)
max_val_adj = np.max(cubic_int) 

row = 2020
row_spec = cubic_int[row:row+1,::]
row_spec = row_spec.flatten()

max_spec = np.max(row_spec[612:617])
half_max = max_spec/2

#%%
# PLOTTING

slit_dim_range=[-6.45, 6.45] 
wavelen_range=[540, 668]
min_val=0
max_val=4000

image_name = "cubic_interp_"+folder_name
image_path = os.path.join(cubic_int_dir, image_name)

fig, ax = plt.subplots(1,1)

ax.imshow(cubic_int, extent=[wavelen_range[0], wavelen_range[1], slit_dim_range[0], slit_dim_range[1]], 
            aspect='auto', cmap='gray_r',  vmin=min_val, vmax=max_val)

# ax.imshow(cubic_int, extent=[wavelen_range[0], wavelen_range[1], 2048, 0], 
#             aspect='auto', cmap='gray_r',  vmin=min_val, vmax=max_val)

ax.set_xlabel('Wavelength [nm]')
ax.set_ylabel('Slit position [mm]')
fig.tight_layout()
# ax.set_ylabel('Slit position [mm]')

fig.savefig(image_path, dpi=300)

#%%
fig, ax = plt.subplots(1,1)

ax.plot(wavelens, row_spec)
ax.scatter(wavelens, row_spec, c='r')