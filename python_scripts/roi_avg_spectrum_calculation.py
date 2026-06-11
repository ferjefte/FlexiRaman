# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 12:30:13 2025

Script to calculate and plot the average spectrum of a selected ROI (false color NMF-image) togehter with the respective NMF-spectrum.

ROI COORDINATES FILES
The coordinates fo the ROIs should be a ".txt" file saved on the "NMF/roi_selections" folder. The order of the files goes accordingly with
the color order, i.e., "roi_coords_01.txt"-->"red", "roi_coords_02.txt"-->"green", and "roi_coords_03.txt"-->"blue". 

NMF RESULTS
Special care should be taken when assigning a color to each NMF-spectrum. It should have the same color as the corresponding ROI.
NMF algorith does not have an specific order when calculating the components.

PLOTING
When ploting the order of the spectra from bottom to top is: R,G,B.
Spectra are normalized for comparison reazons.  

TIFF IMAGE WITH ROIS
The NMF-image is also displayed with the respective ROIs. The size of the image must be controlled so when exporting it has the same size
as the NMF-image (check "dpi" value).

@author: aguilafernando
"""

import os
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# FOLDER NAMES AND DIRECTORIES
project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")


# date = '20250717'
date = '20250523'
# date = '20250516'

# sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'
# sample = 'Volt'

ROI = '03'
# ROI = '02'

test = '01'

subfolder = r"2025-08-11_19-35-21_c5" # date = '20250523'
# subfolder = r"2025-08-07_17-41-01_c5" # date = '20250516'
# subfolder = r"2025-08-12_13-25-28_c5" # date = '20250717'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

cubic_int_dir = os.path.join(working_directory, 'cubic_interpolation_python')

roi_path = "NMF\\"+subfolder+"\\roi_selections"
roi_coord_dir = os.path.join(working_directory, roi_path)

# folder for the storage of the averaging of the ROIs
avg_dir = os.path.join(working_directory, "rois_average_data")

try:
    os.mkdir(avg_dir)
    print(f"Created: {avg_dir}")
except FileExistsError:
    print(f"Already exists: {avg_dir}")

# GAUSS CORRECTION MATRIX PATH
gauss_correction_name = 'horizontal_gauss_correction_matrix_'+sample+'_'+date+'.npy'
gauss_matrix_path = os.path.join(data_directory, gauss_correction_name)

#%%
# LOADING ROI COORDINATES

# LOADING FILE NAMES
# # here I am just loading the names of the .txt files that contain the coordinates of the corners of the selection rectangle per ROI selected

files_coord = []

for item in os.listdir(roi_coord_dir):
    item_path = os.path.join(roi_coord_dir,item)
    
    if os.path.isfile(item_path) and item.endswith('.txt'):
        files_coord.append(item_path)
        
# RETRIEVEING COORDINATES PER FILE
# # here I am reading all the coordinates of the four corners of the selection rectangle per ROI selected in the image

coords_dic = {}

# read each line and make a list that contains a list per line
for i,path in enumerate(files_coord):    
    with open(path, 'r') as file:
        lines = [l.strip().split('\t') for l in file.readlines()] # read lines (.readlines()) and removes "\n" (.strip()) makes a list by removing "\t" (.split())
    
    # convert the coordinates into integers
    for l in range(1,len(lines)):
        for j in range(2):
            lines[l][j]=int(lines[l][j])
        
    coords_dic[i] = lines    
    
    # # visualization
    # for l in lines:
    #     print(l)
    # print(coords_dic[0][1][0])

#%%    
# LOADING THE CUBIC INTERPOLATED IMAGES 
# # here I am loading all the cubic interpolated images corresponding to the ROI selected per ROI in coords_dic

roi_imgs = {}

# runs over the rois
for i in range(len(coords_dic)):
    
    # load the corresponding interpolated images
    fir_img_idx = coords_dic[i][1][1]
    last_img_idx = coords_dic[i][3][1]
    idx_array = np.arange(fir_img_idx, last_img_idx+1)
    
    temp_imgs = np.empty((len(idx_array),2048,2048), dtype=np.int32 )
    
    # runs over the image files amount of the selected roi
    for j,file in enumerate(idx_array):
        path = os.path.join(cubic_int_dir, f'image_{file:0{4}d}.npy')
        temp_imgs[j,:,:] = np.load(path)
    
    roi_imgs[f'ROI{i}'] = temp_imgs

#%%
# AVERAGE SPECTRUM CALCULATION
# # here I calculate the avg spectrum of the corresponding ROI for every ROI in roi_imgs

roi_avgs = {}

# Runs over the ROIS
for i in range(len(roi_imgs)):
    
    firs_row = coords_dic[i][1][0]
    last_row = coords_dic[i][2][0]
    idx_array = np.arange(firs_row, last_row+1)
    
    avg_per_img = []

    num_imgs = len(roi_imgs[f'ROI{i}'])
    
    # Runs over the images in the corresponding ROI
    for j in range(num_imgs):
        
        selection = roi_imgs[f'ROI{i}'][j][firs_row:last_row+1, :]
        avg_selec = np.mean(selection, axis=0)
        avg_per_img.append(avg_selec)
        
    avg_spec = np.mean(avg_per_img, axis=0)
    
    # saving raw average of ROI as numpy file
    avg_path = os.path.join(avg_dir, f"ROI_0{i+1}_avg.npy")
    avg_path_txt = os.path.join(avg_dir, f"ROI_0{i+1}_avg.txt")
    np.save(avg_path, avg_spec)
    np.savetxt(avg_path_txt, avg_spec)
    
    avg_spec = (avg_spec - np.min(avg_spec)) /np.max(avg_spec) 
    
    roi_avgs[f'ROI{i}'] = avg_spec

#%%    
# plot test of average 
test_avg = np.load( os.path.join(avg_dir, "ROI_03_avg.npy") )

fig, ax=plt.subplots(1,1)
ax.plot(test_avg)

#%%
# LOADING RESULTS FROM NMF

Pfad = working_directory

jj = 199
PfadNMF = Pfad +"\\NMF"
Bildpfad = PfadNMF + "\\"+ subfolder
subBildpfad = Bildpfad + "\\W_RGBjj" + str(jj).zfill(5)
########## read NMF_info.txt #######################################################
NMF_info = {}

# LOAD NUMPY PLOTS
HH=np.load(Bildpfad+"\\H_jj"+str(jj).zfill(5)+".npy")

# # FOR 20250516_Pig01_C_ROI02_test01
# red_plot = HH[0]
# green_plot = HH[1]
# blue_plot = HH[2]

# FOR 20250717_PS3_3_ROI03_test01
red_plot = HH[2]
green_plot = HH[0]
blue_plot = HH[1]

# # FOR 20250523_Pig01_C_ROI03_test01
# red_plot = HH[1]
# green_plot = HH[2]
# blue_plot = HH[0]

# Normalization
red_plot = ( red_plot-np.min(red_plot) ) / np.max(red_plot)
green_plot = ( green_plot-np.min(green_plot) ) / np.max(green_plot)
blue_plot = ( blue_plot-np.min(blue_plot) ) / np.max(blue_plot)

rgb_plots = [red_plot, green_plot, blue_plot]

# LOADING NMF PARAMETER VALUES
# Die Datei öffnen und zeilenweise lesen
with open(Bildpfad +"\\NMFinfo_jj" +str(jj).zfill(5)+ ".txt", "r") as file:
    for line in file:
        key, value = line.strip().split("\t") # Zeile in Key und Value aufteilen
        NMF_info[key] = value # Key-Value-Paar im Dictionary speichern
        
ui_LaserWL = float(NMF_info["ui_LaserWL"])
ui_ScaleLow = float(NMF_info["ui_ScaleLow"])
ui_ScaleHigh = float(NMF_info["ui_ScaleHigh"])
ui_Channels = int(NMF_info["ui_Channels"])
firstchannel = int(NMF_info["firstchannel"])
lastchannel = int(NMF_info["lastchannel"])
res_xy = float(NMF_info["resolution_xy"])

scale = np.linspace(ui_ScaleLow, ui_ScaleHigh, ui_Channels, endpoint=True)
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale

# save wavenumbers/wavelengths arrays
wavelen_arr_path = os.path.join(data_directory, "wavelen_arr.npy")
wavelen_arr_txt_path = os.path.join(data_directory, "wavelen_arr.txt")
wavenum_arr_path = os.path.join(data_directory, "wavenum_arr.npy")
wavenum_arr_txt_path = os.path.join(data_directory, "wavenum_arr.txt")

np.save(wavelen_arr_path , scale)
np.savetxt(wavelen_arr_txt_path , scale)
np.save(wavenum_arr_path , scale_cm1)
np.savetxt(wavenum_arr_txt_path , scale_cm1)

#%%
# PLOTTING RESULTS

colors = ['orangered', 'lime', 'cyan']
colors_plots = ['r', 'g', 'b']

fig, ax = plt.subplots(1,1, figsize=(9,7))
plt.rcParams['font.size'] = 14
for k in range(len(roi_avgs)):
    ax.plot(scale_cm1[firstchannel:lastchannel+1],  roi_avgs[f'ROI{k}']*2+3*k+0.6, label=f'ROI {k+1}', color = colors_plots[k])
    ax.plot(scale_cm1[firstchannel:lastchannel+1],  rgb_plots[k]*2+3*k, label=f'Comp. {k+1}', color = colors_plots[k], ls=':')

# test comparing last ROI with protein spectral component
# ax.plot(scale_cm1[firstchannel:lastchannel+1],  roi_avgs[f'ROI{2}']*2+3*2+0.6, label=f'ROI {3}', color = colors_plots[2])
# ax.plot(scale_cm1[firstchannel:lastchannel+1],  rgb_plots[2]*2+3*2, label=f'Comp. {3}', color = colors_plots[0], ls=':')

# plt.axhline(y=0, color='gray', linestyle=':')
plt.axhline(y=0.6, color='gray', linestyle='--', lw=0.7)
plt.axhline(y=3, color='gray', linestyle='--', lw=0.7)
plt.axhline(y=3.6, color='gray', linestyle='--', lw=0.7)
plt.axhline(y=6, color='gray', linestyle='--', lw=0.7)
plt.axhline(y=6.6, color='gray', linestyle='--', lw=0.7)
ax.spines['bottom'].set_position('zero')
plt.legend(ncol=3, loc='upper center', borderaxespad=0)
plt.xlabel("Wavenumber [$cm^{-1}$]")
plt.ylabel("Intensity [arb.]")
plt.yticks([])
plt.grid(linestyle='--')
plt.ylim(0,10)
plt.xlim(240,3860)
fig.tight_layout()
Pfad_plotout=Bildpfad + "\\ROIS_spectra" 
plt.savefig(Pfad_plotout+".tiff", format="png", dpi=300)

#%%        
# TIFF IMAGE DISPLAY

# ARRANGING COORDINATES FOR PLOTTING (https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html#matplotlib.patches.Rectangle)
plot_rect_coords = {}
for i,c in enumerate(coords_dic):
    x = int(coords_dic[c][4][0])
    y = int(coords_dic[c][4][1])
    width = coords_dic[c][3][0]-x
    height = coords_dic[c][1][1]-y
    plot_rect_coords[c] = [x, y, width, height]
    # print(x,y,width,height)

# SHOWING OF TIFF IMAGE WITHSELECTED ROIs


loadRaTiffFile = tf.TiffFile(subBildpfad+'.tiff') #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
rgb_img = loadRaTiffFile.pages[0].asarray()
rgb_img = np.int32(rgb_img)

# PIXELS PER INCH PPI
ppi_w = (2048/(2202.91/24))

# case 20250523_PS3_3_ROI03_test01
ppi_l = (1002/(2202.91/24)) # #_pixels_image / (diagonal_pixels/diagonal_inches)

# # case 20250516_Pig01_C_ROI02_test01
# ppi_l = (601/(2202.91/24)) # #_pixels_image / (diagonal_pixels/diagonal_inches)

# Create a figure with that exact size and no padding
fig = plt.figure(figsize=(ppi_w,ppi_l),  frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.]) # [left, bottom, width, height] in relative coordinates
ax.set_axis_off() # Turn off the axis
fig.add_axes(ax)

# # FOR 20250717_PS3_3_ROI03_test01
# GAUSSIAN CORRECTION
gauss_matrix = np.load(gauss_matrix_path)

# # fig, ax = plt.subplots(1,1, figsize=(22,22), frameon=False)
# gauss_matrix = gauss_matrix.T
rgb_img[:,:,0] = rgb_img[:,:,0]/gauss_matrix
rgb_img[:,:,1] = rgb_img[:,:,1]/gauss_matrix
rgb_img[:,:,2] = rgb_img[:,:,2]/gauss_matrix
# ax.imshow(rgb_img[0:2048,:,:])

ax.imshow(rgb_img)

for c,i in enumerate(plot_rect_coords):
    x = plot_rect_coords[i][0]
    y = plot_rect_coords[i][1]
    w = plot_rect_coords[i][2]
    h = plot_rect_coords[i][3]
    rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor=colors[c], facecolor='none')

    # Add the rectangle to the plot
    ax.add_patch(rect)
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
# plt.tight_layout(pad=0)

# SAVING TIFF IMAGE
Pfad_imout=Bildpfad + "\\W_RGB_ROISjj" + str(jj).zfill(5)

# FOR 20250523_Pig01_C_ROI03_test01/20250516_Pig01_C_ROI02_test01
plt.savefig(Pfad_imout+".tiff", format="png", dpi=107, pad_inches=0, bbox_inches='tight')

# # FOR 20250717_PS3_3_ROI03_test01
# plt.savefig(Pfad_imout+".tiff", format="png", dpi=200, pad_inches=0, bbox_inches='tight')

# tf.imwrite(rgb_img[0:2048,:,:], sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/res_xy, 1/res_xy), metadata={"spacing": res_xy, 'unit': 'mm', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work

# plt.close(fig) 
        