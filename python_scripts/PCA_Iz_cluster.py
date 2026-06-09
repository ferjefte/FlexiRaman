# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:20:22 2026

@author: hauswaldwalter

PCA

This script loads the data from Izabellas measurements using the Witec setup


Important Parameters to define are:
-date 
-sample
-ROI
-test 
-n_comp # number of PCA components

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
from loadIntImg_cluster import loadIzaImg

########## change parameters here #################################################################

script_directory = os.path.dirname(os.path.abspath(__file__))

project_directory = os.path.dirname(script_directory)
data_directory = os.path.join(project_directory, "data")

# date = '20260513'
date = '20260505'

sample = 'PS3_3'

# ROI = '02'
ROI = '01'

test = '01'
# test = '02'

folder_name = date+"_"+sample+"_ROI"+ROI+"_test"+test

Pfad = os.path.join(project_directory, folder_name)
DataPfad = os.path.join(Pfad,'raw')


n_comp = 6; # Number of PCA components

#res_xy = 0.0065/(50/180*100)  #xy pixel size
Bittype=np.float32 # Attention Imagej does not know 16 bit RGB format

########## read Raman spectral channel tiff #######################################################
undistortion_info = {}
# undistortion_info = parameter_reader(Pfad_data +"/parameters_interpolation.txt")
# res_xy = float(undistortion_info["ResolutionXY"])
# undistortion_info = parameter_reader(Pfad +"/Scan_002 Information.txt") # for date = '20260513'
undistortion_info = parameter_reader(Pfad +"/Scan_006 Information.txt") # for date = '20260505'
res_xy = float(undistortion_info["ResolutionXY [um]:"])
ui_LaserWL = float(undistortion_info["Excitation Wavelength [nm]:"])


PfadPCA = Pfad +"/PCA"

RaTxtliste = [f for f in os.listdir(DataPfad) if f.endswith(".txt") ]
filename = DataPfad +"/"+ RaTxtliste[0] 
numtiffimg = len(RaTxtliste)

wln, M, Mshape = loadIzaImg(filename) # wavelengths array [1/cm], Matrix with all the data, Shape of matrix (n,m)


ui_Channels = Mshape[1]
ui_ScaleLow = wln[0]
ui_ScaleHigh = wln[-1]
firstchannel = 0
lastchannel = ui_Channels 
ROIxMin = 0
ROIxMax = int(undistortion_info["Lines per Image:"])

#normiere
minX=np.min(M)
M=np.clip(M,0,10000000000) # clip zeros
maxM=np.max(M)
M=M/maxM

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

pca.fit(M)
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
    ax.plot(wln, H[i]+i*0.2, label=f"comp. {i}",linewidth=1)

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
W = np.matmul(M, Minv) #unmixed = single(A)*Minv;

for ii in range (0,n_comp): # save all W vectors as a tiff images in ..\3D-cutproject\PCA\DateTime\
    print("save W ii ",ii+1," of ",n_comp)
    tf.imwrite(subBildpfad+"/W_"+str(ii).zfill(5)+".tif", 
               W[:,ii].reshape((100,100)).astype(Bittype), 
               imagej=True, 
               resolution=(res_xy, res_xy), 
               resolutionunit='MICROMETER', 
               metadata={ "unit": "um", "axes": "YX", "mode": "grayscale"})

np.save(Bildpfad+"/H.npy", H)

# save wln array
wln_path = os.path.join(Bildpfad, 'wln')
np.save(wln_path, wln)

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
    datei.write(f"Data_normalization\t{maxM}\n")
    datei.write(f"Data_clip\t{minX}\n")
    datei.write(f"PCA_components\t{n_comp}\n")
    datei.write(f"PCA_SVD.solver\t{pca.svd_solver}\n")
    datei.write(f"PCA_reconstruction_error\t{PCAerror}\n")
    datei.write(f"PCA_computing_time_s\t{end - start}\n")
    datei.write(f"ui_ScaleLow\t{ui_ScaleLow}\n")
    datei.write(f"ui_ScaleHigh\t{ui_ScaleHigh}\n")
    datei.write(f"ui_Channels\t{ui_Channels}\n")
    datei.write(f"ui_LaserWL\t{ui_LaserWL}\n")