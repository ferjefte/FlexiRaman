#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:30:10 2024

SCRIPT TO PERFORM:
    -> CALIBRATION OPTIMIZATION
    -> DARK IMAGES AVERAGING
    -> INTERPOLATION OF CALIBRATION
    -> VISUALIZATION OF INTERPOLATION AND SPECTRA

@author: fernandoaguila
"""

## ALL THE STEPS OF IMAGE PROCESSING IN ONE PROGRAMM
from calibration_raw_img_process import background_average
from calibration_optimization_visual import (opt_visual, interpolation_python_visual, 
                                                             spectrum_visual)
from calib_n_ord_terms_optimization import hyperspec_calibration
# from hyperspec_calib_norderterms_optimization_gpt_f import hyperspec_calibration
from calibration_interpolation import flexram_interp_calib
import os 
from parameter_reader import parameter_reader, parameter_reader_slit
from pathlib import Path

# FILE NAMES AND DIRECTORIES


project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")
calib_param_directory = os.path.join(project_directory, "20260106_Neon_lamp_test01", "calibration_data" )



# date = '20240906'
# date = '20251029'
# date = '20260105'
# date = '20260106'
# date = '20260519'
date = '20260522'


# sample = 'Neon_lamp'
sample = 'Pig01_C'

# ROI = '02'
ROI = '04'


test = '01'

slit = 'B1'

# RAW MEASUREMENTS DIRECTORY
# folder_name =  date+'_'+sample+'_test'+test
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# DARK BACKGROUND AVERAGE FILE PATH
# dark_folder_name ='20250520_dark'
dark_folder_name = 'dark'
dark_directory = os.path.join(working_directory, dark_folder_name)

# # Case when dark images change due to different exposure time
# measur_folder_name = '\\filter'
# dark_folder_name ='dark'
# dark_directory = os.path.join(working_directory+measur_folder_name, dark_folder_name)

# GENERAL PARAMETERS 
general_parameters_path = os.path.join(data_directory, 'parameters_interpolation.txt')
gen_param_dic = parameter_reader(general_parameters_path)

calib_slit_date = gen_param_dic['calib_slit_date']
order = gen_param_dic['order']
umethod = gen_param_dic['umethod']
file_ext = gen_param_dic['file_ext']

slit_adj_path = os.path.join(data_directory, 'slit_adjustments.txt')
slit_adj_dic = parameter_reader_slit(slit_adj_path)


yi0_adj = float(slit_adj_dic[slit][0])
rot_adj = float(slit_adj_dic[slit][1])
xi0_adj = float(slit_adj_dic[slit][2])

# # # B1 slit mask adjustments (FR2022_4)
# yi0_adj = 0
# rot_adj = -0.22
# xi0_adj = 0
#%%
# DARK BACKGROUND AVERAGING FOR REGULAR MEASUREMENTS
background_average(dark_directory)

#%%
### OPTIMIZATION 
hyperspec_calibration(
        working_directory,
        order,
        # neon_file_name='neon_lines_calibration_02052024.txt',
        neon_file_name='neon_lines_calibration_06012026.txt',
        slit_length=12.9,
        slit_sep=0.3,
        optimization_method='Powell',
        optimization_tolerance=1e-8
    )

#%%
### VISUALISATION OF OPTIMIZATION 
opt_visual(calib_param_directory, order)

#%%
## INTERPOLATION OF CALIBRATED IMAGE
flexram_interp_calib(working_directory, calib_param_directory, order, umethod, xi0_adj, yi0_adj, rot_adj, 'img_hi_processed.npy')

#%%
## INTERPOLATION VISUALIZATION 
interpolation_python_visual(working_directory, 0, umethod, min_val=0, max_val=4000)

#%%
## PLOT OF THE RAMAN SPECTRUM AND RAMAN SHIFT OF THE SELECTED SECTION OF THE INTERPOLATED IMAGES

spectrum_visual(working_directory, working_directory+'\\calibration_data',
                umethod,
                image_number=0, 
                row_u=934, 
                row_l=1035)



