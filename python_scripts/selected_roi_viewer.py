# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 11:53:56 2025

@author: aguilafernando
"""

import numpy as np
import os
import matplotlib.pyplot as plt
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
# roi_folder = os.path.join(working_directory, "cubic_interpolation_python")
roi_folder = os.path.join(working_directory, "cubic_interpolation_roi_python")

image_path = os.path.join(roi_folder, "image_0000.npy")
image = np.load(image_path)

fig, ax = plt.subplots(1,1)
ax.imshow(image)
