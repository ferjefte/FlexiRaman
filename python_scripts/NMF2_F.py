# -*- coding: utf-8 -*-
"""
Created on Tue May 20 13:56:53 2025

@author: hauswaldwalter

Like NMF1 but this time intermediate results are saved - the maximum number of iterations is given by: "miter" * "loopiter"

This script loads a batch of tiff images under the directory: "Pfad" in the subdirectory "\tiff" and it loads information from a file “undistortion_info.txt” in "Pfad".
This information is read depending on: imagetype. The imagetype is: "SpXY" or "XYSp"
"SpXY" stands for undistorted tiff images with X: Spectral information and Y: X-information. The image stack itself runs along the Y axis.
"XYSp" stands for undistorted tiff images with X: X-information and Y: Y-information. These images are created after a reslice. The image stack itself runs along the Spectral axis.

Important Parameters to define a ROIU are:
firstchannel = 80 #0
lastchannel = 1999 #2047
ROIxMin = 0 #512
ROIxMax = 2047 #1535
Use them to select ROIS. small ROIs use less memory. Cut a bit from the spectra to avoid  misleading information from the edge.

In this script, the iterative NMF is executed in "loopiter" steps.
The maximum number of iterations is given by: "miter" * "loopiter"
The number of component to find is given by: "n_comp"
At the end there is a result which is written to the pathNMF directory

The results are:
"W_ .tif": distribution maps of the components found
"H_ .np": an np array with the component spectra found
"H_ .png": plots of the component spectra found with scale from information from undistortion_info.txt
"NMFinfo_ .txt": a summary of interesting parameters about the NMF and the spectra which may be interesting for later evaluation

Example of: "undistortion_info.txt":
LaserWL	532.0
ScaleLow	540.0
ScaleHigh	668.0
Channels	2048
"""

import os
import tifffile as tf # https://pypi.org/project/tifffile/  # open Terminal of environment in Anaconda and type: pip install "tifffile" / for LZW: pip install "imagecodecs"
import numpy as np
import sys
import time # for debugging only
import datetime
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF # install scikit-learn in your conda environment
from parameter_reader import parameter_reader

########## change parameters here #################################################################

project_directory =  r"D:\Projekte\Flexiraman\Fernando"
Pfad_data = r'D:\Projekte\Flexiraman\Fernando\data'

# date = '20250507'
date = '20260518'

sample = 'Pig01_C'

roi = '00'

test = '01'

folder_name = date+"_"+sample+"_ROI"+roi+"_test"+test

Pfad_interp = os.path.join(project_directory, folder_name)
Pfad_data = r"D:\Projekte\Flexiraman\Fernando\data"
imagetype = "SpXY" # select wether the image contains "XYSp" Data (after reslice) or "SpXY" (after undistortion without reslice) Data
n_comp = 5; # Number of NMF components
miter = 10; # Max Number of total NMF iterations
loopiter = 200; # Max Number of loops
res_xy = 0.0065/(50/180*100)  #xy pixel size
Bittype=np.float32 # Attention Imagej does not know 16 bit RGB format
firstchannel = 80#0
lastchannel = 1999 #2047 #9 #2047
nnRaSpCh=lastchannel-firstchannel+1
ROIxMin = 250 #512
ROIxMax = 1100 #1535 #2047 #3087 #1535
ROIxPx = ROIxMax - ROIxMin + 1

########## read undistortion_info.txt #######################################################
undistortion_info = {}

# Die Datei öffnen und zeilenweise lesen

# with open(Pfad_data +"\\parameters_interpolation.txt", "r") as file:
#     for line in file:
#         key, value = line.strip().split("\t") # Zeile in Key und Value aufteilen
#         undistortion_info[key] = value # Key-Value-Paar im Dictionary speichern

undistortion_info = parameter_reader(Pfad_data +"\\parameters_interpolation.txt")
# print(undistortion_info)
ui_LaserWL = float(undistortion_info["LaserWL"])
ui_ScaleLow = float(undistortion_info["wavelen_left"])
ui_ScaleHigh = float(undistortion_info["wavelen_right"])
ui_Channels = int(undistortion_info["m"])
scale = np.linspace(ui_ScaleLow, ui_ScaleHigh, ui_Channels, endpoint=True)
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale

########## read Raman spectral channel tiff #######################################################
PfadRaTiff = Pfad_interp +"\\interpolation_tif" #specify Raman spectral channel Data source here
PfadNMF = Pfad_interp +"\\NMF"
RaTiffliste = os.listdir(PfadRaTiff)
numtiffimg = len(RaTiffliste)
       
if (imagetype == "SpXY"): #images after undistortion only contain X: spectral information, Y: X information
    print("Number of available tiff images (Y Pixel):",numtiffimg) # Y
    #test load to get shape
    fileRaTiff=PfadRaTiff +"\\"+ RaTiffliste[0] #file names
    testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
    testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
    loadshape=testloadRaTiff.shape                    # (X Sp)
    print("SpXY images with shape (X Sp):",loadshape)

    #numspectra=numtiffimg*loadshape[0]         # Y * X
    numspectra=numtiffimg*ROIxPx                # Y * ROI(X)
    ROIshape = [numtiffimg,ROIxPx]              # Y, ROI(X)
    
    if ((ROIxMax >= loadshape[0]) or (ROIxMin > ROIxMax)): # number of tiff images in Pfad +"\\tiff"
         print("Es sind nur",loadshape[0],"Scannzeilen in einem Bild vorhanden. ROIxMin:",ROIxMin,"oder ROIxMax:",ROIxMax,"sind zu groß.")
         sys.exit() # Skript abbrechen
    if ((lastchannel >= loadshape[1]) or (firstchannel > lastchannel)): # number of tiff images in Pfad +"\\tiff"
        print("Es sind nur",loadshape[1],"Spektralkanäle in einem Bild vorhanden. firstchannel:",firstchannel,"oder lastchannel:",lastchannel,"sind zu groß.")
        sys.exit() # Skript abbrechen

    X = np.zeros((numspectra, nnRaSpCh))

    print("load",numtiffimg,"images:")
    for ii in range (0,numtiffimg): # Y: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
        print("load ii ",ii+1," of ",numtiffimg)
        fileRaTiff=PfadRaTiff +"\\"+ RaTiffliste[ii] #file names
        loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
        loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
        X[(ROIxPx*ii):(ROIxPx*(ii+1)),:]=loadRaData[ROIxMin:(ROIxMax+1),firstchannel:(lastchannel+1)] # (Y*ROI(X), ROI(Sp)) = (ROI(X), ROI(Sp))

elif (imagetype == "XYSp"): #images after reslice contain X: X information, Y: Y information
    if ((lastchannel >= numtiffimg) or (firstchannel > lastchannel)): # number of tiff images in Pfad +"\\tiff"
        print("Es sind nicht genug Bilder im Quellordner vorhanden bzw. firstchannel oder lastchannel ist zu groß")
        sys.exit() # Skript abbrechen
    print("Number of available tiff images (spectral channels):",numtiffimg) # Sp
    #test load to get shape
    fileRaTiff=PfadRaTiff +"\\"+ RaTiffliste[firstchannel] #file names
    testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
    testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
    loadshape=testloadRaTiff.shape                    # (Y X)
    print("XYSp images with shape (Y X):",loadshape)

    #numspectra=loadshape[0]*loadshape[1]             # Y * X
    numspectra=loadshape[0]*ROIxPx                    # Y * ROI(X)
    ROIshape = [loadshape[0],ROIxPx]                  # Y, ROI(X)

    X = np.zeros((numspectra, nnRaSpCh))

    print("load",nnRaSpCh,"images (spectral channels):")
    #for ii in range (0,nnRaSpCh): # loop over all tiff images in ..\3D-cutproject\RaSpChdata\
    for ii in range (firstchannel,lastchannel+1): # Sp: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
        print("load ii ",ii+1-firstchannel," of ",nnRaSpCh)
        fileRaTiff=PfadRaTiff +"\\"+ RaTiffliste[ii] #file names
        loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
        loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
        X[:,ii-firstchannel]=loadRaData[:,ROIxMin:(ROIxMax+1)].flatten()  # (Y*ROI(X), ROI(Sp)) = (Y, ROI(X))

#normiere
minX=np.min(X)
X=np.clip(X,0,10000000000) # clip zeros
maxX=np.max(X)
X=X/maxX

#Bereite Speichpfade vor
if not os.path.exists(PfadNMF):
    os.makedirs(PfadNMF)
jetztstr=datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
Bildpfad = PfadNMF + "\\"+ jetztstr+ "_c"+str(n_comp)
os.mkdir(Bildpfad) # create subfolder with currend date time

########## setup NMF #################################################################

# https://scikit-learn.org/dev/modules/generated/sklearn.decomposition.NMF.html
#model = NMF(n_components=n_comp, init="random", solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=miter, random_state=0) # for reproducable noise
#model = NMF(n_components=n_comp, init="random", solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=miter, random_state=None)
#model = NMF(n_components=n_comp, init="nndsvd", solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=miter, random_state=None)
model = NMF(n_components=n_comp, init="nndsvdar", solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=miter, random_state=None)
#model = NMF(n_components=n_comp, init="nndsvdar", solver="mu", beta_loss="frobenius", tol=0.0001, max_iter=miter, random_state=None)

########## do the NMF stepwise #################################################################

for jj in range (0,loopiter):
    ########## do some iterations of the NMF #################################################################
    
    start = time.time() # for debugging only
    
    if jj == 0:
        WW = model.fit_transform(X)
        HH = model.components_
    else:
        model.init="custom"
        WW = model.fit_transform(X,W=WW, H=HH)
        HH = model.components_
    
    end = time.time() # to measure the NMF computing time - for debugging only
    
    ########## process/save the results of the NMF #############################################
    subBildpfad = Bildpfad + "\\W_jj" + str(jj).zfill(5)
    os.mkdir(subBildpfad) # create subfolder with currend date time
    
    for ii in range (0,n_comp): # save all W vectors as a tiff images in ..\3D-cutproject\NMF\DateTime\
        print("save W ii ",ii+1," of ",n_comp)
        tf.imwrite(subBildpfad+"\\W_"+str(ii).zfill(5)+".tif",WW[:,ii].reshape(ROIshape).astype(Bittype), imagej=True, resolution=(1/res_xy, 1/res_xy), metadata={"spacing": res_xy, "unit": "mm", "axes": "YX", "mode": "grayscale"})
    
    np.save(Bildpfad+"\\H_jj"+str(jj).zfill(5)+".npy", HH)
    
    # plotting
    fig, ax = plt.subplots(1)
    fig.set_size_inches(8, 5)
    for i in range(0,n_comp):
        ax.plot(scale_cm1[firstchannel:lastchannel+1],HH[i], label=f"comp. {i}",linewidth=1)
    
    plt.legend()
    plt.xlabel("Wavenumber $/cm^{-1}$")
    plt.ylabel("Intensity /arb.")
    plt.title(str(n_comp) + " component spectra obtained with NMF")
    plt.xlim(0, 4000)
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.savefig(Bildpfad+"\\H_plot_jj"+str(jj).zfill(5)+".png", format="png", dpi=300)
    plt.close()
    
    NMFerror = model.reconstruction_err_
    print ("NMF reconstruction error:" + str(NMFerror))
    NMFiter = model.n_iter_
    print ("NMF iterations:" + str(NMFiter))
    print("NMF successfully completed in: ", end - start," s") # for debugging only
    
    #save interesting numbers:
    with open(Bildpfad+"\\NMFinfo_jj"+str(jj).zfill(5)+".txt", "w") as datei:
        datei.write(f"firstchannel\t{firstchannel}\n")
        datei.write(f"lastchannel\t{lastchannel}\n")
        datei.write(f"ROIxMin\t{ROIxMin}\n")
        datei.write(f"ROIxMax\t{ROIxMax}\n")
        datei.write(f"resolution_xy\t{res_xy}\n")
        datei.write(f"Data_normalization\t{maxX}\n")
        datei.write(f"Data_clip\t{minX}\n")
        datei.write(f"NMF_components\t{n_comp}\n")
        datei.write(f"NMF_model.init\t{model.init}\n")
        datei.write(f"NMF_model.solver\t{model.solver}\n")
        datei.write(f"NMF_model.beta_loss\t{model.beta_loss}\n")
        datei.write(f"NMF_reconstruction_error\t{NMFerror}\n")
        datei.write(f"NMF_iterations\t{NMFiter}\n")
        datei.write(f"NMF_computing_time_s\t{end - start}\n")
        datei.write(f"ui_LaserWL\t{ui_LaserWL}\n")
        datei.write(f"ui_ScaleLow\t{ui_ScaleLow}\n")
        datei.write(f"ui_ScaleHigh\t{ui_ScaleHigh}\n")
        datei.write(f"ui_Channels\t{ui_Channels}\n")