# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 11:13:24 2025

@author: hauswaldwalter

PCA

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

In this script, the PCA is calculated followed by a (Moore-Penrose) pseudo-inverse to calculate additionally component maps.
The number of component to find is given by: "n_comp"
At the end there is a result which is written to the pathPCA directory

The results are:
"W_ .tif": distribution maps of the components found
"H_ .np": an np array with the component spectra found
"H_ .png": plots of the component spectra found with scale from information from undistortion_info.txt
"PCAinfo_ .txt": a summary of interesting parameters about the PCA and the spectra which may be interesting for later evaluation

Example of: "undistortion_info.txt":
LaserWL	532.0
ScaleLow	540.0
ScaleHigh	668.0
Channels	2048
"""


import os
import tifffile as tf # https://pypi.org/project/tifffile/  # open Terminal of environment in Anaconda and type: pip install "tifffile" / for LZW: pip install "imagecodecs"
import numpy as np
import time # for debugging only
import datetime
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA # install scikit-learn in your conda environment
from parameter_reader import parameter_reader
from loadIntImg_cluster import loadIntImg

########## change parameters here #################################################################

project_directory = r'D:\Projekte\Flexiraman\Fernando'
Pfad_data = r'D:\Projekte\Flexiraman\Fernando\data'


# date = '20250717'
#date = '20250523'
#date = '20250516'
#date = '20260107'
date = '20260518'

sample = 'Pig01_C'
# sample = 'PS3_3'

# roi = '03'
#roi = '02'
#roi = '01'
roi = '00'

test = '01'

folder_name = date+"_"+sample+"_ROI"+roi+"_test"+test

Pfad = os.path.join(project_directory, folder_name)

imagetype = "SpXY" # select wether the image contains "XYSp" Data (after reslice) or "SpXY" (after undistortion without reslice) Data
filetype = "npy" # filetype = "tif"
n_comp = 5; # Number of PCA components
#miter = 5; # Max Number of total NMF iterations

#res_xy = 0.0065/(50/180*100)  #xy pixel size
Bittype=np.float32 # Attention Imagej does not know 16 bit RGB format
firstchannel = 0
lastchannel = 2047 
nnRaSpCh=lastchannel-firstchannel+1
ROIxMin = 0
ROIxMax = 2047

########## read undistortion_info.txt #######################################################
undistortion_info = {}

undistortion_info = parameter_reader(Pfad_data +"/parameters_interpolation.txt")
# print(undistortion_info)
ui_LaserWL = float(undistortion_info["LaserWL"])
ui_ScaleLow = float(undistortion_info["wavelen_left"])
ui_ScaleHigh = float(undistortion_info["wavelen_right"])
ui_Channels = int(undistortion_info["m"])

res_xy = float(undistortion_info["ResolutionXY"])
scale = np.linspace(ui_ScaleLow, ui_ScaleHigh, ui_Channels, endpoint=True)
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale

########## read Raman spectral channel tiff #######################################################
#PfadRaTiff = Pfad +"/tiff" #specify Raman spectral channel Data source here
if (filetype == "tif"):
    PfadRaTiff = Pfad +"/interpolation_tif" # Fernando Neu
elif (filetype == "npy"):
    PfadRaTiff = Pfad +"/cubic_interpolation_python"
PfadPCA = Pfad +"/PCA"

X, ROIshape = loadIntImg(PfadRaTiff,imagetype,filetype,firstchannel,lastchannel,nnRaSpCh,ROIxMin,ROIxMax)

#normiere
minX=np.min(X)
X=np.clip(X,0,10000000000) # clip zeros
maxX=np.max(X)
X=X/maxX

#Bereite Speichpfade vor
if not os.path.exists(PfadPCA):
    os.makedirs(PfadPCA)
jetztstr=datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
Bildpfad = PfadPCA + "/"+ jetztstr+ "_c"+str(n_comp)
os.mkdir(Bildpfad) # create subfolder with currend date time
subBildpfad = Bildpfad + "/W"
os.mkdir(subBildpfad) # create subfolder with currend date time

########## setup PCA #################################################################

# https://scikit-learn.org/dev/modules/generated/sklearn.decomposition.PCA.html

#class sklearn.decomposition.PCA(n_components=None, *, copy=True, whiten=False, svd_solver='auto', tol=0.0, iterated_power='auto', n_oversamples=10, power_iteration_normalizer='auto', random_state=None):
#pca = PCA(n_components=n_comp, svd_solver='full')
pca = PCA(n_components=n_comp, svd_solver='auto')

########## do the PCA #################################################################

start = time.time() # for debugging only

pca.fit(X)
VR = pca.explained_variance_ratio_
SV = pca.singular_values_  #SV**2/VR = const
VA = pca.explained_variance_
H = pca.components_

end = time.time() # to measure the PCA computing time - for debugging only

########## process/save the results of the PCA #############################################
# Stelle sicher, dass die Arrays die gleiche Länge haben
if len(VR) != len(SV) or len(VR) != len(VA):
    raise ValueError("Die Arrays müssen die gleiche Länge haben.")

zeilen_index = np.arange(len(VR))
daten = np.column_stack((zeilen_index, VR, SV, VA))
np.savetxt(Bildpfad+"/PCAres.txt", daten, delimiter=",", header="Index,VR,SV,VA")

# plotting
fig, ax = plt.subplots(1)
fig.set_size_inches(8, 5)
for i in range(0,n_comp):
    ax.plot(scale_cm1[firstchannel:lastchannel+1],H[i]+i*0.2, label=f"comp. {i}",linewidth=1)

plt.legend()
plt.xlabel("Wavenumber $/cm^{-1}$")
plt.ylabel("Intensity /arb.")
plt.title(str(n_comp) + " component spectra obtained with PCA")
plt.xlim(0, 4000)
#plt.xlim(500, 1500)
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig(Bildpfad+"/H_plot.png", format="png", dpi=300)
#plt.savefig(Bildpfad+"/H_plot5001500.png", format="png", dpi=300)
plt.close()

# (Moore-Penrose) pseudo-inverse
Minv = np.linalg.pinv(H) #Minv=pinv(h); Compute the (Moore-Penrose) pseudo-inverse of a matrix.
W = np.matmul(X, Minv) #unmixed = single(A)*Minv;

for ii in range (0,n_comp): # save all W vectors as a tiff images in ..\3D-cutproject\PCA\DateTime\
    print("save W ii ",ii+1," of ",n_comp)
    tf.imwrite(subBildpfad+"/W_"+str(ii).zfill(5)+".tif",W[:,ii].reshape(ROIshape).astype(Bittype), imagej=True, resolution=(res_xy, res_xy), metadata={"spacing": res_xy, "unit": "mm", "axes": "YX", "mode": "grayscale"})

np.save(Bildpfad+"/H.npy", H)

# NMFerror = model.reconstruction_err_
PCAerror = 0 # think later how to calculate this out of H X and W
# print ("NMF reconstruction error:" + str(NMFerror))
# NMFiter = model.n_iter_
# print ("NMF iterations:" + str(NMFiter))
print("PCA successfully completed in: ", end - start," s") # for debugging only

#save interesting numbers:
with open(Bildpfad+"/PCAinfo.txt", "w") as datei:
    datei.write(f"firstchannel\t{firstchannel}\n")
    datei.write(f"lastchannel\t{lastchannel}\n")
    datei.write(f"ROIxMin\t{ROIxMin}\n")
    datei.write(f"ROIxMax\t{ROIxMax}\n")
    datei.write(f"resolution_xy\t{res_xy}\n")
    datei.write(f"Data_normalization\t{maxX}\n")
    datei.write(f"Data_clip\t{minX}\n")
    datei.write(f"PCA_components\t{n_comp}\n")
    datei.write(f"PCA_SVD.solver\t{pca.svd_solver}\n")
    datei.write(f"PCA_reconstruction_error\t{PCAerror}\n")
    datei.write(f"PCA_computing_time_s\t{end - start}\n")
    datei.write(f"ui_LaserWL\t{ui_LaserWL}\n")
    datei.write(f"ui_ScaleLow\t{ui_ScaleLow}\n")
    datei.write(f"ui_ScaleHigh\t{ui_ScaleHigh}\n")
    datei.write(f"ui_Channels\t{ui_Channels}\n")
