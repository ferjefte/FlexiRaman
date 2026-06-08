# -*- coding: utf-8 -*-
"""
Created on Wed May 21 16:23:22 2025

@author: hauswaldwalter

This script helts to prepare coustum RGB images for print reproduction using "W_ .tif" files.
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

########## change parameters here #################################################################

Pfad = r"E:\MultiHoloDiag\AP31_GrundlegendeVoruntersuchungen_WalterLydia\Versuchsreihe 19\20211027 MHD VR19 Laser"
Pfad = r"E:\FlexiRaman\2025-05-07 Schweinehaut"
subfolder = r"2025-05-21_17-27-22_c5"
jj = 199
PfadNMF = Pfad +"\\NMF"
Bildpfad = PfadNMF + "\\"+ subfolder
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

AllImg = np.zeros((loadshape[0], loadshape[1], numtiffimg))
    
for ii in range (0,numtiffimg): # Y: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
    print("load ii ",ii+1," of ",numtiffimg)
    fileRaTiff=subBildpfad +"\\"+ RaTiffliste[ii] #file names
    loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
    loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
    AllImg[:,:,ii]=loadRaData # (Y*ROI(X), ROI(Sp)) = (ROI(X), ROI(Sp))

########## write RGB tiff #######################################################

sImg = np.zeros((loadshape[0], loadshape[1], 3))

# CHANGE CHANNELS HERE:
# Take a gamma of 0.45 to correspond approximately to the sRGB gamma https://en.wikipedia.org/wiki/SRGB
sImg[:,:,0] = ContrastGamma(AllImg[:,:,0],0,np.max(AllImg[:,:,0]),outMin,outMax,gamma) #Red
sImg[:,:,1] = ContrastGamma(AllImg[:,:,1],0,np.max(AllImg[:,:,1]),outMin,outMax,gamma) #Green
sImg[:,:,2] = ContrastGamma(AllImg[:,:,2],0,np.max(AllImg[:,:,2]),outMin,outMax,gamma) #Blue

Pfad_imout=Bildpfad + "\\W_RGBjj" + str(jj).zfill(5)
tf.imwrite(Pfad_imout+".tiff", sImg.astype(Bittype), photometric='rgb', imagej=tiftypeimagej, resolution=(1/res_xy, 1/res_xy), metadata={"spacing": res_xy, 'unit': 'mm', 'axes': 'YXS', 'mode': 'rgb'}) # Walter is not shure about the axiy definition but XY does not work