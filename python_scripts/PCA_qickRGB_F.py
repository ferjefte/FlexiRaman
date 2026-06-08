
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 12:42:49 2026

@author: aguilafernando

This script helts to prepare coustum RGB images for print reproduction using "W_ .tif" files.
Necessary information is read from "PCAinfo_ .txt"
Channels are quick and dirty selected in the block:
    sImg[:,:,0] = ContrastGamma(AllImg_PCA[:,:,0],0,np.max(AllImg_PCA[:,:,0]),outMin,outMax,gamma) #Red
    sImg[:,:,1] = ContrastGamma(AllImg_PCA[:,:,1],0,np.max(AllImg_PCA[:,:,1]),outMin,outMax,gamma) #Green
    sImg[:,:,2] = ContrastGamma(AllImg_PCA[:,:,2],0,np.max(AllImg_PCA[:,:,2]),outMin,outMax,gamma) #Blue
below
Do not forgett to also adjust the channel in np.max(AllImg_PCA[:,:,0]!
"""

########## import ####################################################################################
import os
import tifffile as tf # https://pypi.org/project/tifffile/  # open Terminal of environment in Anaconda and type: pip install "tifffile" / for LZW: pip install "imagecodecs"
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

########## change parameters here #################################################################
# FOLDER NAMES AND DIRECTORIES

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

# date = '20250717'
# date = '20250523'
# date = '20250516'
# date = '20260107'
# date = '20260518'
# date = '20260505'
# date = '20260513'
# date = '20260519'
# date = '20260520'
date = '20260522'

# sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'
# sample = 'Volt'

# ROI = '03'
# ROI = '01'
# ROI = '02'
# ROI = '00'
ROI = '04'

test = '01'
# test = '02'

# subfolder = r"2026-01-13_13-54-50_c5" # date = '20250523' 
# subfolder = r"2026-01-14_18-29-29_c7" # date = '20250523' 
# subfolder = r"2026-01-13_14-31-09_c5" # date = '20250516' 
# subfolder = r"2026-01-14_18-36-19_c7" # date = '20250516' 
# subfolder = r"2026-01-15_11-36-33_c5" # date = '20250717' 
# subfolder = r"2026-01-14_17-01-26_c7" # date = '20250717' 
# subfolder = r"2026-06-01_14-16-59_c6" # date = '20260107' 
# subfolder = r"2026-01-13_11-12-08_c5" # date = '20260107' 
# subfolder = r"2026-01-14_18-48-46_c7" # date = '20260107'
# subfolder = r"2026-06-01_14-29-58_c6" # date = '20260513'
# subfolder = r"2026-05-18_16-36-20_c5" # date = '20260518' 
# subfolder = r"2026-05-13_14-26-05_c5" # date = '20260505' 
# subfolder = r"2026-06-01_14-34-28_c6" # date = '20260505' 
# subfolder = r"2026-05-21_15-49-05_c5" # date = '20260519'
# subfolder = '2026-06-01_14-05-38_c6' # date = '20260519
# subfolder = r"2026-05-26_16-53-46_c5" # date = '20260520' 
# subfolder = r'2026-06-01_13-52-10_c6' # date = '20260520'
# subfolder = r"2026-05-26_17-34-48_c5" # date = '20260522'
subfolder = r'2026-06-01_13-21-59_c6' # date = '20260522'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

Pfad = working_directory


PfadPCA = Pfad +"\\PCA"
Bildpfad = PfadPCA + "\\"+ subfolder

case_ = 'no_gauss'
# case_ = 'gauss'

if case_ == 'gauss':
    subBildpfad = Bildpfad + f"\\W_{case_}"
    
else:
    subBildpfad = Bildpfad + "\\W" 
    


gamma = 0.45 # use 1 for lineal imaging, use 0.45 to compensate for 2.2 screen gamma (sRGB) and make images apear linear on screen or print https://en.wikipedia.org/wiki/SRGB
Bittype=np.uint8 # Attention Imagej does not know 16 bit RGB format
if (Bittype==np.uint8):
    outMax=255 # out White level
    tiftypeimagej=True
if (Bittype==np.uint16):
    outMax=65535 # out White level
    tiftypeimagej=False
outMin=0


#%%

########## def ####################################################################################


def ContrastGamma (ImgIn,min_in,max_in,min_out,max_out,gamma): #raw converter
    #ImgIn:    input image
    #min_in:   minimum input level (to be projected to min_out), typ: cammera dark level or a little higher
    #max_in:   maximum input level (to be projected to min_out), typ: level of brightest region of image
    #min_out:  typ: 0
    #max_out:  typ: 255 or 65535
    #gamma:    use 1 to gain a linear result, use 1/2.2 to compensate for monitor gamma of 2.2
    return (np.clip((ImgIn.astype(np.float32)-min_in)/(max_in-min_in),0,1)**gamma)*(max_out-min_out)+min_out; # viel Zeit brauchen **gamma und np.clip !!!
    #return        (((ImgIn.astype(np.float32)-min_in)/(max_in-min_in))    **gamma)*(max_out-min_out)+min_out; #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ohne clip
    #https://numpy.org/devdocs/user/quickstart.html
    #https://stackoverflow.com/questions/14448763/is-there-a-convenient-way-to-apply-a-lookup-table-to-a-large-array-in-numpy

########## linear maping to sRGB maping #######################################################

def linear2srgb(lin): #vereinfachte Funktion für Skalen (in: 0 - 1)
    img = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.power(lin, 1.0 / 2.4) - 0.055)
    return np.clip(img, 0.0, 1.0)

#%%
# COLOR MAPS DEFINITION
 # lin2sRGB Transfer function
ncolors = 256
color_array = np.ones([ncolors,4])#plt.get_cmap('gist_rainbow')(range(ncolors))

# change RGB values
linScale = np.linspace(0.0,1.0,ncolors)
#bwr color_array[:,0] = np.clip(linScale*2,0,1) # R
#bwr color_array[:,1] = np.clip(1-np.abs(linScale*2-1),0,1) # G
#bwr color_array[:,2] = np.clip(2-linScale*2,0,1) # B
#bwr color_array[:,3] = 1 # A
color_array[:,0] = linear2srgb(linScale*2-1) # R
color_array[:,1] = np.abs(linScale*2-1)
color_array[:,2] = linear2srgb(2-linScale*2-1) # B
color_array[:,3] = 1 # A
# create a colormap object
map_object = LinearSegmentedColormap.from_list(name='CyBuBkRdYe_Nl',colors=color_array)
# register this new colormap with matplotlib
plt.colormaps.register(cmap=map_object,force=True)

# FERNANDO MODIFICATION
# color_array[:,0] = np.abs(linScale*2-1) # R
# color_array[:,1] = linear2srgb(2-linScale*2-1)
# color_array[:,2] = linear2srgb(linScale*2-1) # B
color_array[:,0] = linear2srgb(linScale*2-1) # R
color_array[:,1] = linear2srgb(2-linScale*2-1)
color_array[:,2] = linear2srgb(linScale*2-1) # B
color_array[:,3] = 1 # linear2srgb(linScale) # A
# create a colormap object
map_object = LinearSegmentedColormap.from_list(name='CyBuBkRdYe_Nl_F',colors=color_array)
# register this new colormap with matplotlib
plt.colormaps.register(cmap=map_object,force=True)


#%%
########## read PCA_info.txt #######################################################

PCA_info = {}

# Die Datei öffnen und zeilenweise lesen
with open(Bildpfad +"\\PCAinfo" + ".txt", "r") as file:
    for line in file:
        key, value = line.strip().split("\t") # Zeile in Key und Value aufteilen
        PCA_info[key] = value # Key-Value-Paar im Dictionary speichern

print(PCA_info)
ui_LaserWL = float(PCA_info["ui_LaserWL"])
ui_ScaleLow = float(PCA_info["ui_ScaleLow"])
ui_ScaleHigh = float(PCA_info["ui_ScaleHigh"])
ui_Channels = int(PCA_info["ui_Channels"])
firstchannel = int(PCA_info["firstchannel"])
lastchannel = int(PCA_info["lastchannel"])
res_xy = float(PCA_info["resolution_xy"])
ROIxMin = int(PCA_info["ROIxMin"])
ROIxMax = int(PCA_info["ROIxMax"])
n_comp = int(PCA_info["PCA_components"])

nnRaSpCh=lastchannel-firstchannel+1
ROIxPx = ROIxMax - ROIxMin + 1
scale = np.linspace(ui_ScaleLow, ui_ScaleHigh, ui_Channels, endpoint=True)
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale

########## read PCA channel tiff #######################################################
RaTiffliste = os.listdir(subBildpfad)
numtiffimg = len(RaTiffliste)
print("Number of available tiff images (PCA components):",numtiffimg) # Y
#test load to get shape
fileRaTiff=subBildpfad +"\\"+ RaTiffliste[0] #file names
testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
loadshape=testloadRaTiff.shape                    # (X Sp)
print("SpXY images with shape (X Sp):",loadshape)

AllImg_PCA = np.zeros((loadshape[0], loadshape[1], numtiffimg))

    
for ii in range (0,numtiffimg): # Y: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
    print("load ii ",ii+1," of ",numtiffimg)
    fileRaTiff=subBildpfad +"\\"+ RaTiffliste[ii] #file names
    loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
    loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
    AllImg_PCA[:,:,ii]=loadRaData # (Y*ROI(X), ROI(Sp)) = (ROI(X), ROI(Sp))
    
# all_min = np.min(AllImg_PCA)
# all_max = np.max(AllImg_PCA)

# zero_position = (0 - all_min) / (all_max - all_min)
    
#%%

# CREATE DIVERGING COLOR MAP WITH POSITIVES RED, NEGATIVES BLUE, AND ZEROS WHITE

def create_diverging_cmap(zero_position, name='my_BuRd', neg_color='blue', zero_color='white', pos_color='red'):
    """Create a custom diverging colormap"""
    colors = [(0.0, neg_color), (zero_position, zero_color), (1.0, pos_color)]
    return LinearSegmentedColormap.from_list(name, colors)

# my_cmap = create_diverging_cmap()
# PLOT THE IMAGES IN A SINGLE COLUMN 
plot_num = [0,0,1,1,2,2]

pixel_x_ticks = np.arange(0, loadshape[1], 500)
x_ticks_labels = [int(pixel_x_ticks[i]*0.234) for i in range(len(pixel_x_ticks))] # um
pixel_y_ticks = np.arange(0, loadshape[0], 500)
y_ticks_labels = [int(pixel_y_ticks[i]*0.234) for i in range(len(pixel_y_ticks))] # um

# cmap = 'bwr'
cmap = 'CyBuBkRdYe_Nl'
# cmap = 'CyBuBkRdYe_Nl_F'
# cmap = 'RdBu'

fig, ax = plt.subplots(3, 2, figsize=(6.5,9), sharex='col', sharey='row')
plt.suptitle(f"PCA Components plot {case_}")
for i in range(numtiffimg):
    
    ind = i%2
    img_i = AllImg_PCA[:,:,i] 
    # max and min per image
    i_max = np.max(img_i)
    i_min = np.min(img_i)
    # print(i_max)
    # if i_min >= 0:
    #     my_cmap = 'Reds'
    # else:
    #     zero_pos = np.abs((0 - i_min) / (i_max - i_min))
    #     my_cmap = create_diverging_cmap(zero_pos)
    
    # quantile
    flat_img = np.abs(img_i.flatten())
    low_q = np.quantile(flat_img, 0.01)
    high_q = np.quantile(flat_img, 0.99)
    
    img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap, vmin=-high_q, vmax=high_q)
    # img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap, vmin=-i_max/4, vmax=i_max/4)
    cbar = plt.colorbar(img_plot, ax=ax[plot_num[i],ind], shrink=0.75)
    
    #ploting
    # if i_min > 0:
    #     img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap)
    #     cbar = plt.colorbar(img_plot, ax=ax[plot_num[i],ind], shrink=0.75)
    
    # else:
    #     img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap, vmin=-high_q, vmax=high_q)
    #     # img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap, vmin=-i_max/4, vmax=i_max/4)
    #     cbar = plt.colorbar(img_plot, ax=ax[plot_num[i],ind], shrink=0.75)
        
    if i%2==1:
        cbar.set_label("Intensity [a.u.]")
    ax[plot_num[i],ind].set_xticks(pixel_x_ticks, x_ticks_labels)
    ax[plot_num[i],ind].set_yticks(pixel_y_ticks, y_ticks_labels)
    # ax[plot_num[i],ind].set_yticks(pixel_ticks, ticks_labels)
    # ax[plot_num[i],ind].set_yticks(pixel_ticks, ticks_labels)
    ax[plot_num[i],ind].set_xlabel("")
    ax[plot_num[i],ind].set_ylabel("")
    
for i in range(3):
    ax[i,0].set_ylabel(r"$\mu$m")
    
for i in range(2):
    ax[2,i].set_xlabel(r"$\mu$m")
    
fig.tight_layout()

plt.savefig(Bildpfad+"\\PCA_H_grid_cmap_plot"+f"_{n_comp}c_{folder_name}_{case_}_{cmap}.png", format="png", dpi=300)


