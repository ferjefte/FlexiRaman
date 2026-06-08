#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:30:10 2024

SCRIPT TO PERFORM:
    -> CALIBRATION
    -> DARK IMAGES AVERAGING
    -> INTERPOLATION OF CALIBRATION
    -> VISUALIZATION OF INTERPOLATION AND SPECTRA

@author: fernandoaguila
"""

## ALL THE STEPS OF IMAGE PROCESSING IN ONE PROGRAMM
from calibration_raw_img_process import background_average
from hyperspec_calibration_optimization_visual_gpt_f import (opt_visual, interpolation_python_visual, 
                                                             spectrum_visual)
from calib_n_ord_terms_optimization import hyperspec_calibration
# from hyperspec_calib_norderterms_optimization_gpt_f import hyperspec_calibration
from hyperspec_calibration_interpolation_gpt_f import flexram_interp_calib
import os 
from parameter_reader import parameter_reader

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

date = '20240906'
# date = '20250514'


sample = 'Neon_lamp'


test = '01'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# DARK BACKGROUND AVERAGE FILE PATH
dark_folder_name ='20250520_dark'
dark_directory = os.path.join(project_directory, dark_folder_name)

# CALIBRATION RAW IMAGES DIRECTORY
# folder_name_calib = '20240906_Neon_lamp_test01'
# calib_imgs_directory = os.path.join(project_directory, folder_name_calib)
# CALIBRATION PARAMETERS SAVING NAMES
# calib_param_directory = os.path.join(data_directory, 'Calibration_06092024')
# calib_param_directory = os.path.join(working_directory, 'calibration_data')
calib_param_file_save_name='C4slit_20240906'

# GENERAL PARAMETERS 
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
gen_param_dic = parameter_reader(general_parameters_path)

calib_slit_date = gen_param_dic['calib_slit_date']
order = gen_param_dic['order']
umethod = gen_param_dic['umethod']
file_ext = gen_param_dic['file_ext']

#%%
# DARK BACKGROUND AVERAGING FOR REGULAR MEASUREMENTS
background_average(dark_directory)

#%%
### OPTIMIZATION 
hyperspec_calibration(
        working_directory,
        order,
        file_name=calib_param_file_save_name,
        neon_file_name='neon_lines_calibration_slitmask02052024.txt',
        slit_length=12.9,
        slit_sep=0.3,
        optimization_method='Powell',
        optimization_tolerance=1e-8
    )

#%%
### VISUALISATION OF OPTIMIZATION 
opt_visual(calib_param_directory, calib_param_file_save_name, order)

#%%
## INTERPOLATION OF CALIBRATED IMAGE
flexram_interp_calib(calib_param_directory, calib_param_file_save_name, folder_name_calib, order, umethod)

#%%
## VISUALIZATION OF A PYTHON INTERPOLATED IMAGE
interpolation_python_visual(calib_imgs_directory, 263, order, 
                            min_val=0, 
                            max_val=1000)

#%%
## PLOT OF THE RAMAN SPECTRUM AND RAMAN SHIFT OF THE SELECTED SECTION OF THE INTERPOLATED IMAGES

spectrum_visual(calib_imgs_directory, data_directory,
                order,
                image_number=200, 
                row_u=934, 
                row_l=1035)



