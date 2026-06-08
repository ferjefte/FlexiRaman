# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 14:50:31 2025

PROGRAM TO SELECT DISPLAY ROI OF A XY-IMAGE AND THE SPECTRAL AVERAGE OF THAT 
REGION 

@author: aguilafernando
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import tifffile as tf
import os

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

date = '20250516'
# date = '20250514'

# sample = 'PS3_P'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'

ROI = '02'

test = '01'

img_number = ['1449', '2939.25']

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

# PLOT AVERAGES ROI DIRECTORY
avg_directory = os.path.join(working_directory, 'roi_plot_avgs')

# NMF FOLDER
nmf_folder = os.path.join(working_directory, 'NMF')
# nmf_results_folder = os.path.join(nmf_folder, '2025-06-05_14-36-29_c5') #
nmf_results_folder = os.path.join(nmf_folder, '2025-05-21_17-27-22_c5_res_for_Fernando')
jj=199

#%%

# LOADING WAVELENGTHS
wavelen_path_name = os.path.join(data_directory, 'wavelengths.npy')
wavelen = np.load(wavelen_path_name)
# raman shift 
wavelen_shift = 1e7/532 - (1e7/wavelen)
wavelen_shift_short = wavelen_shift[80:2000]

# LAODING FALSE COLOR IMAGE
image_directory = os.path.join(working_directory, 'XY_python')
image_path = os.path.join(image_directory, img_number[0]+'_resliced_image_'+sample+'_test'+test+'_'+img_number[1]+'.npy')
image = np.load(image_path)
image2 = mpimg.imread( os.path.join(working_directory, 'W_RGBjj00199_sb.jpg') )

#%%
# LISTING COORDINATES FILES AND AVG-PLOT FILES
files = os.listdir(avg_directory)

coord_files = [f for f in files if f.endswith("coord.txt")]

plot_files = [f for f in files if f.endswith("spectra.txt")]

# SAVING THE DATA FROM THE TXT FILES
coords_dic = {}
plots_dic = {}

# RETRIVEING COORDINATES
for i,f in enumerate(coord_files):
    name = os.path.join(avg_directory, f)
    with open(name, 'r') as file:
        lines = [l.strip().split('\t') for l in file]
        coords_dic[f'roi0{i+1}']=lines[1:]

# ARRANGING COORDINATES FOR PLOTTING (https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html#matplotlib.patches.Rectangle)
plot_rect_coords = {}
for i,c in enumerate(coords_dic):
    x = int(coords_dic[c][0][0])
    y = int(coords_dic[c][0][1])
    width = int(coords_dic[c][2][1])-y
    height = int(coords_dic[c][1][0])-x
    plot_rect_coords[c] = [x, y, width, height]
        
# RETRIVEING PLOTS
for i,f in enumerate(plot_files):
    name = os.path.join(avg_directory, f)
    with open(name, 'r') as file:
        lines = [l.strip().split('\t') for l in file]
        plots_dic[f'roi0{i+1}']=lines[1:]

# SELECTING ONLY THE AVERAGE OF THE INTENSITY AND NORMALIZING       
plot_avg = {}
for i,p in enumerate(plots_dic):
    avg_data = [np.float16(j[1]) for j in plots_dic[p]]
    max_val = np.max(avg_data)
    min_val = np.min(avg_data)
    avg_data = (avg_data - min_val)/(max_val - min_val)
    plot_avg[p] = avg_data
    
#%%
# RETREIVING NMF COMPONENTS RESULTS
nmf_array_path = os.path.join(nmf_results_folder, f'H_jj{jj:0{5}d}.npy')
nmf_array = np.load(nmf_array_path)

# # NORMALIZING
# nmf_n, nmf_m = np.shape(nmf_array)
# for i in range(nmf_n):
#     vals = nmf_array[i,:]
#     max_val = np.max(vals)
#     min_val = np.min(vals)
#     nmf_array[i,:] = (vals - min_val)/(max_val-min_val)
    
#%%
# PLOTTING
color = ['y', 'g', 'tab:purple', 'b', 'r', 'm'] 
# offset = np.linspace(0,20,5, dtype=int)
offset = np.zeros((5))
order_measured = [3, 0, 1, 4, 2]
spec_left_lim = 80
spec_right_lim = 2000


# MAKING A DICTIONARY OF BOTH MEASURED AND CALCULATED PLOTS ASSOCIATED WITH COLOR
plot_dic = {}
for i,j in enumerate(order_measured):
    # plot_dic[f'comp{i:0{2}d}'] = [ 4*plot_avg[f'roi{j+1:0{2}d}'][spec_left_lim:spec_right_lim]+offset[i], nmf_array[i]++offset[i] ]
    plot_dic[f'comp{i:0{2}d}'] = [ plot_avg[f'roi{j+1:0{2}d}'][spec_left_lim:spec_right_lim]+offset[i], nmf_array[i]++offset[i] ]


#%%
# SHOWING OF TIFF IMAGE WITHSELECTED ROIs
fig, ax = plt.subplots(1,1)
ax.imshow(image2)

for c,i in enumerate(order_measured):
    x = plot_rect_coords[f'roi{i+1:0{2}d}'][0]
    y = plot_rect_coords[f'roi{i+1:0{2}d}'][1]
    w = plot_rect_coords[f'roi{i+1:0{2}d}'][2]
    h = plot_rect_coords[f'roi{i+1:0{2}d}'][3]
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color[c], facecolor='none')

    # Add the rectangle to the plot
    ax.add_patch(rect)
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
    
# SAVING
tif_img_path = os.path.join(avg_directory, 'tif_image_rois.tif')
fig.savefig(tif_img_path, format='tiff', dpi=400)

#%%
# PLOTTING OF AVERAGE SPECTRA


for i,j in enumerate(plot_dic): 
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    ax.set_title('Average spectra of selected ROI')
    ax.plot(wavelen_shift_short, plot_dic[j][0], color=color[i], label = 'Measured')
    ax.plot(wavelen_shift_short, plot_dic[j][1], color=color[i], ls='--', label='NMF')
    ax.legend()
    # ax.set_yticks([])    
    ax.set_xlabel('Raman shift [1/cm]')
    ax.set_ylabel('Counts [a.u.]')
    ax.set_ylim(bottom=0)

# Fernando's way
# first_w = int(wavelen_shift[0])
# last_w = int(wavelen_shift[-1])
# ax.set_xlim(left=first_w, right=last_w)
# x_ticks = np.linspace(first_w, last_w, 8, dtype=int)
# x_ticks_labels = [str(i) for i in x_ticks]

# Izabella's way
first_w = 270
last_w = 3800
ax.set_xlim(left=first_w, right=last_w)
x_ticks = [270, 700, 1200, 1700, 2200, 2700, 3200, 3700]
x_ticks_labels = [str(i) for i in x_ticks]


ax.set_xticks(x_ticks, x_ticks_labels)

# SAVING
spec_path = os.path.join(avg_directory, 'average_spectra.tif')
fig.savefig(spec_path, format='tiff', dpi=400)