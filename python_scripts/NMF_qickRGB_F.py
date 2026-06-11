# -*- coding: utf-8 -*-
"""
Created on Wed May 21 16:23:22 2025

@author: hauswaldwalter

This script helps to prepare coustum RGB images for print reproduction using "W_ .tif" files.
Necessary information is read from "NMFinfo_ .txt"
Channels are quick and dirty selected in the block:
    sImg[:,:,0] = ContrastGamma(AllImg[:,:,0],0,np.max(AllImg[:,:,0]),outMin,outMax,gamma) #Red
    sImg[:,:,1] = ContrastGamma(AllImg[:,:,1],0,np.max(AllImg[:,:,1]),outMin,outMax,gamma) #Green
    sImg[:,:,2] = ContrastGamma(AllImg[:,:,2],0,np.max(AllImg[:,:,2]),outMin,outMax,gamma) #Blue
below
Do not forgett to also adjust the channel in np.max(AllImg[:,:,0]!
"""

########## import ####################################################################################
import os
import tifffile as tf # https://pypi.org/project/tifffile/  # open Terminal of environment in Anaconda and type: pip install "tifffile" / for LZW: pip install "imagecodecs"
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from pathlib import Path

########## change parameters here #################################################################
# FOLDER NAMES AND DIRECTORIES

project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")



# date = '20250717'
# date = '20250523'
# date = '20250516'
# date = '20260107'
# date = '20260505'
# date = '20260513'
date = '20260519'
# date = '20260520'
# date = '20260522'


# sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'
# sample = 'Volt'

# ROI = '03'
# ROI = '01'
ROI = '02'
# ROI = '04'


# test = '02'
test = '01'

# subfolder = r"2025-08-11_19-35-21_c5" # date = '20250523' five
# subfolder = "2026-01-15_10-01-08_c7"  # date = '20250523' seven
# subfolder = r"2025-08-07_17-41-01_c5" # date = '20250516' five
# subfolder = r"2026-01-15_15-03-22_c7" # date = '20250516' seven
# subfolder = r"2025-08-12_13-25-28_c5" # date = '20250717' five
# subfolder = r"2026-01-14_16-32-05_c7" # date = '20250717' seven
# subfolder = r"2026-01-09_13-31-32_c5" # date = '20260107' five
# subfolder = r"2026-04-27_14-59-07_c7" # date = '20260107' seven # corrected for horizontal shift 
# subfolder = r"2026-05-12_15-48-30_c7" # date = '20260505' 
# subfolder = r"2026-05-19_17-37-21_c7" # date = '20260513' 
# subfolder = r"2026-05-20_13-29-04_c7" # date = '20260513' 
# subfolder = r"2026-05-22_13-57-34_c7" # date = '20260513' 
subfolder = r'2026-05-20_13-29-04_c7' # date = '20260519'
# subfolder = r"2026-05-26_16-55-12_c7" # date = '20260522'

# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

Pfad = working_directory

# jj = 184 # date = '20250516'
# jj = 199 # date = '20250523' / '20250717'
jj = 169 # date = '20260107' seven comp.
PfadNMF = Pfad +"\\NMF"
Bildpfad = PfadNMF + "\\"+ subfolder

case_ = 'no_gauss'
# case_ = 'gauss'

if case_ == 'gauss':
    subBildpfad = Bildpfad + "\\W_jj" + str(jj).zfill(5) + "_gauss"
    
    
else:
    subBildpfad = Bildpfad + "\\W_jj" + str(jj).zfill(5)    
    
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

def FrameClip (ImgIn,corner_ul,corner_lr,sx,sy): #selects a shifted ROI of an image
    #ImgIn:     input image
    #corner_ul: upper left corner of ROI in pixel coordinates Y,X
    #corner_lr: lower right corner of ROI in pixel coordinates Y,X
    #sx:        shift in x direction
    #sy:        shift in y direction
    if (corner_lr[0] == -1): # take whole image 
        corner_lr[0] = ImgIn.shape[0]
    if (corner_lr[1] == -1): # take whole image 
        corner_lr[1] = ImgIn.shape[1]
    height = corner_lr[0] - corner_ul[0]
    width = corner_lr[1] - corner_ul[1]

    h = corner_ul[0]+sy        # Y
    if (h<0):                  # Y
        resy1 = -h
        iny1 = 0
    else:
        resy1 = 0
        iny1 = h
        
    h = corner_ul[1]+sx        # X
    if (h<0):                  # X
        resx1 = -h
        inx1 = 0
    else:
        resx1 = 0
        inx1 = h
        
    h = corner_lr[0]+sy        # Y
    if (h>=ImgIn.shape[0]):    # Y
        resy2 = ImgIn.shape[0]-(corner_ul[0]+sy)
        iny2 = ImgIn.shape[0]
    else:
        resy2 = height
        iny2 = h
        
    h = corner_lr[1]+sx        # X
    if (h>=ImgIn.shape[1]):    # X
        resx2 = ImgIn.shape[1]-(corner_ul[1]+sx)
        inx2 = ImgIn.shape[1]
    else:
        resx2 = width
        inx2 = h
        
    res = np.zeros([height,width],ImgIn.dtype) 
    #res = ImgIn[corner_ul[0]+sy:corner_lr[0]+sy,corner_ul[1]+sx:corner_lr[1]+sx] # without crossing the border
    res[resy1:resy2,resx1:resx2] = ImgIn[iny1:iny2,inx1:inx2]
    return res

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

########## read NMF_info.txt #######################################################
NMF_info = {}

# Die Datei öffnen und zeilenweise lesen
with open(Bildpfad +"\\NMFinfo_jj" +str(jj).zfill(5)+ ".txt", "r") as file:
    for line in file:
        key, value = line.strip().split("\t") # Zeile in Key und Value aufteilen
        NMF_info[key] = value # Key-Value-Paar im Dictionary speichern

print(NMF_info)
ui_LaserWL = float(NMF_info["ui_LaserWL"])
ui_ScaleLow = float(NMF_info["ui_ScaleLow"])
ui_ScaleHigh = float(NMF_info["ui_ScaleHigh"])
ui_Channels = int(NMF_info["ui_Channels"])
firstchannel = int(NMF_info["firstchannel"])
lastchannel = int(NMF_info["lastchannel"])
res_xy = float(NMF_info["resolution_xy"])
ROIxMin = int(NMF_info["ROIxMin"])
ROIxMax = int(NMF_info["ROIxMax"])
n_comp = int(NMF_info["NMF_components"])

nnRaSpCh=lastchannel-firstchannel+1
ROIxPx = ROIxMax - ROIxMin + 1
scale = np.linspace(ui_ScaleLow, ui_ScaleHigh, ui_Channels, endpoint=True)
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale

########## read NMF channel tiff #######################################################
RaTiffliste = os.listdir(subBildpfad)
numtiffimg = len(RaTiffliste)
print("Number of available tiff images (NMF components):",numtiffimg) # Y
#test load to get shape
fileRaTiff=subBildpfad +"\\"+ RaTiffliste[0] #file names
testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
loadshape=testloadRaTiff.shape                    # (X Sp)
print("SpXY images with shape (X Sp):",loadshape)

AllImg_NMF = np.zeros((loadshape[0], loadshape[1], numtiffimg))
    
for ii in range (0,numtiffimg): # Y: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
    print("load ii ",ii+1," of ",numtiffimg)
    fileRaTiff=subBildpfad +"\\"+ RaTiffliste[ii] #file names
    loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
    loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
    AllImg_NMF[:,:,ii]=loadRaData # (Y*ROI(X), ROI(Sp)) = (ROI(X), ROI(Sp))


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
cmap = 'viridis'

fig, ax = plt.subplots(3, 2, figsize=(6.5,9), sharex='col', sharey='row')
plt.suptitle(f"NMF components plot {case_}")

for i in range(numtiffimg-1):
    
    ind = i%2
    img_i = AllImg_NMF[:,:,i] 
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
    flat_img = img_i.flatten()
    low_q = np.quantile(flat_img, 0.01)
    high_q = np.quantile(flat_img, 0.99)
    
    img_plot = ax[plot_num[i],ind].imshow(img_i, cmap=cmap, vmin=low_q, vmax=high_q)
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

plt.savefig(Bildpfad+"\\NMF_H_grid_cmap_plot"+f"_{n_comp}c_{folder_name}_{case_}_{cmap}.png", format="png", dpi=300)

#%%
# # PLOT THE IMAGES IN A SINGLE COLUMN BEFORE GAMMA CORRECTION

# fig, ax = plt.subplots(numtiffimg, 1, figsize=(5,10))
# for i in range(numtiffimg):
#     # gamma_img = ContrastGamma(AllImg[:,:,i], 0, np.max(AllImg[:,:,i]), outMin, outMax, gamma)
#     ax[i].imshow(AllImg[:,:,i], cmap='gray')
#     ax[i].tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    
# fig.tight_layout()    
# #%%
# # PLOT THE IMAGES IN A SINGLE COLUMN AFTER GAMMA CORRECTION

# fig, ax = plt.subplots(numtiffimg, 1, figsize=(5,10))
# for i in range(numtiffimg):
#     gamma_img = ContrastGamma(AllImg[:,:,i], 0, np.max(AllImg[:,:,i]), outMin, outMax, gamma)
#     ax[i].imshow(gamma_img, cmap='gray')
#     ax[i].tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    
# fig.tight_layout()


    

#%%
######### write RGB tiff #######################################################

sImg = np.zeros((loadshape[0], loadshape[1], 3))

# RGB COLOR CHANGE 

# # for 20250523_Pig01_C_ROI03_test01
# red = AllImg_NMF[:,:,1]
# green = AllImg_NMF[:,:,2]
# blue = AllImg_NMF[:,:,0]

# # OG convention
# red = AllImg_NMF[:,:,0]
# green = AllImg_NMF[:,:,1]
# blue = AllImg_NMF[:,:,2]

# # for 20250717_PS3_3_ROI03_test01
# red = AllImg_NMF[:,:,2]
# green = AllImg_NMF[:,:,0]
# blue = AllImg_NMF[:,:,1]

# for 20250717_PS3_3_ROI03_test01
red = AllImg_NMF[:,:,1]
green = AllImg_NMF[:,:,5]
blue = AllImg_NMF[:,:,4]

# CHANGE CHANNELS HERE:
# Take a gamma of 0.45 to correspond approximately to the sRGB gamma https://en.wikipedia.org/wiki/SRGB
sImg[:,:,0] = ContrastGamma(red,0,np.max(red),outMin,outMax,gamma) #Red
sImg[:,:,1] = ContrastGamma(green,0,np.max(green),outMin,outMax,gamma) #Green
sImg[:,:,2] = ContrastGamma(blue,0,np.max(blue),outMin,outMax,gamma) #Blue

if case_ == 'gauss':
    Pfad_imout=Bildpfad + "\\W_RGBjj" + str(jj).zfill(5) + '_gauss'
    # tf.imwrite(Pfad_imout+".tiff", sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/res_xy, 1/res_xy), metadata={"spacing": res_xy, 'unit': 'mm', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work
    tf.imwrite(Pfad_imout+".tiff", sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/0.234, 1/0.234), metadata={"spacing": res_xy, 'unit': 'um', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work
    
    

else:
    Pfad_imout=Bildpfad + "\\W_RGBjj" + str(jj).zfill(5)
    # tf.imwrite(Pfad_imout+".tiff", sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/res_xy, 1/res_xy), metadata={"spacing": res_xy, 'unit': 'mm', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work
    tf.imwrite(Pfad_imout+".tiff", sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/0.234, 1/0.234), metadata={"spacing": res_xy, 'unit': 'um', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work




