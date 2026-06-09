# -*- coding: utf-8 -*-
"""
Created on Tue May 27 14:13:31 2025

SCRIPT TO:
    -> VISUALIZE INTERPOLATED SINGLE IMAGES
    -> PERFORM SNIP BASE LINE CORRECTION
    -> VISUALIZING SINGLE SPECTRA  

@author: aguilafernando
"""

from hyperspec_calibration_optimization_visual_gpt_f import (interpolation_python_visual, 
                                                             spectrum_visual)
from SNIP_algorithm import  baseline_correction_images
import os 
from parameter_reader import parameter_reader

script_directory = os.path.dirname(os.path.abspath(__file__))

project_directory = os.path.dirname(script_directory)
data_directory = os.path.join(project_directory, "data")



date = '20250516'
# date = '20250514'

# sample = 'PS3_P'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'

ROI = '02'

test = '01'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# GENERAL PARAMETERS 
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
gen_param_dic = parameter_reader(general_parameters_path)

calib_slit_date = gen_param_dic['calib_slit_date']
order = gen_param_dic['order']
umethod = gen_param_dic['umethod']
file_ext = gen_param_dic['file_ext']

#%%
## VISUALIZATION OF A PYTHON INTERPOLATED IMAGE
interpolation_python_visual(working_directory, 263, order, 
                            min_val=0, 
                            max_val=1000)

#%%
## BASELINE SNIP CORRECTION
baseline_correction_images(working_directory, order, 2, 
                           file_ext='.npy', max_half_window=10)

#%%
# SINGLE OF AVERAGING OF SPECTRUM IN ROI'S
spectrum_visual(working_directory, data_directory, sample, test,
                image_number=570, 
                row_u=984, 
                row_l=985)