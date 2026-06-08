# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 13:34:38 2025

@author: hauswaldwalter
"""
import tifffile as tf # https://pypi.org/project/tifffile/  # open Terminal of environment in Anaconda and type: pip install "tifffile" / for LZW: pip install "imagecodecs"
import numpy as np
import sys
import os


def loadIntImg(PfadRaTiff,imagetype,filetype,firstchannel,lastchannel,nnRaSpCh,ROIxMin,ROIxMax):
    ROIxPx = ROIxMax - ROIxMin + 1
    #RaTiffliste = os.listdir(PfadRaTiff)
    if (filetype == "tif"):
        RaTiffliste = [f for f in os.listdir(PfadRaTiff) if f.endswith(".tif") or f.endswith(".tiff")]  # Nur TIFF-Dateien
    elif (filetype == "npy"):
        RaTiffliste = [f for f in os.listdir(PfadRaTiff) if f.endswith(".npy")]  # Nur TIFF-Dateien
    else:
        return
    numtiffimg = len(RaTiffliste)
    
    if (imagetype == "SpXY"): #images after undistortion only contain X: spectral information, Y: X information
        print("Number of available tiff images (Y Pixel):",numtiffimg) # Y
        #test load to get shape
        fileRaTiff=PfadRaTiff +"/"+ RaTiffliste[0] #file names
        if (filetype == "tif"):
            testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
            testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
        elif (filetype == "npy"):
            testloadRaTiff = np.load(fileRaTiff)  #npy
        loadshape=testloadRaTiff.shape                    # (X Sp)
        print("SpXY images with shape (X Sp):",loadshape)
    
        #numspectra=numtiffimg*loadshape[0]         # Y * X
        numspectra=numtiffimg*ROIxPx                # Y * ROI(X)
        ROIshape = [numtiffimg,ROIxPx]              # Y, ROI(X)
        
        if ((ROIxMax >= loadshape[0]) or (ROIxMin > ROIxMax)): # number of tiff images in Pfad +"/tiff"
             print("Es sind nur",loadshape[0],"Scannzeilen in einem Bild vorhanden. ROIxMin:",ROIxMin,"oder ROIxMax:",ROIxMax,"sind zu groß.")
             sys.exit() # Skript abbrechen
        if ((lastchannel >= loadshape[1]) or (firstchannel > lastchannel)): # number of tiff images in Pfad +"/tiff"
            print("Es sind nur",loadshape[1],"Spektralkanäle in einem Bild vorhanden. firstchannel:",firstchannel,"oder lastchannel:",lastchannel,"sind zu groß.")
            sys.exit() # Skript abbrechen
    
        X = np.zeros((numspectra, nnRaSpCh))
    
        print("load",numtiffimg,"images:")
        for ii in range (0,numtiffimg): # Y: loop over all tiff images in ..\3D-cutproject\RaSpChdata\
            print("load ii ",ii+1," of ",numtiffimg)
            fileRaTiff=PfadRaTiff +"/"+ RaTiffliste[ii] #file names
            if (filetype == "tif"):
                loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
                loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
            elif (filetype == "npy"):
                loadRaData = np.load(fileRaTiff)  #npy
            X[(ROIxPx*ii):(ROIxPx*(ii+1)),:]=loadRaData[ROIxMin:(ROIxMax+1),firstchannel:(lastchannel+1)] # (Y*ROI(X), ROI(Sp)) = (ROI(X), ROI(Sp))
    
    elif (imagetype == "XYSp"): #images after reslice contain X: X information, Y: Y information
        if ((lastchannel >= numtiffimg) or (firstchannel > lastchannel)): # number of tiff images in Pfad +"/tiff"
            print("Es sind nicht genug Bilder im Quellordner vorhanden bzw. firstchannel oder lastchannel ist zu groß")
            sys.exit() # Skript abbrechen
        print("Number of available tiff images (spectral channels):",numtiffimg) # Sp
        #test load to get shape
        fileRaTiff=PfadRaTiff +"/"+ RaTiffliste[firstchannel] #file names
        if (filetype == "tif"):
            testloadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
            testloadRaTiff = testloadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
        elif (filetype == "npy"):
            testloadRaTiff = np.load(fileRaTiff)  #npy
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
            fileRaTiff=PfadRaTiff +"/"+ RaTiffliste[ii] #file names
            if (filetype == "tif"):
                loadRaTiffFile = tf.TiffFile(fileRaTiff) #loads Raman spectral channel tiff but does not immediately convert to numpy array - so tags can still be read
                loadRaData = loadRaTiffFile.pages[0].asarray() # pages selects the page of the tiff file and returns numpy array
            elif (filetype == "npy"):
                loadRaData = np.load(fileRaTiff)  #npy
            X[:,ii-firstchannel]=loadRaData[:,ROIxMin:(ROIxMax+1)].flatten()  # (Y*ROI(X), ROI(Sp)) = (Y, ROI(X))

    return X, ROIshape

def loadIzaImg(DataPfad):
    """
    Read floating point numbers from a tab-separated text file.
    
    Parameters:
    filename (str): Path to the input text file
    
    Returns:
    tuple: (x_values, data_matrix) where:
        - x_values: 1D numpy array of shape (n,) containing first column values
        - data_matrix: 2D numpy array of shape (n, m-1) containing remaining columns
    """
    
    try:
        # Read the entire file, handling tab-separated values
        data = np.loadtxt(DataPfad, delimiter='\t')
        
        # Extract first column as x-axis values
        w_values = data[:, 0]
        
        # Extract remaining columns as the data matrix
        data_matrix = data[:, 1:] # rows = wavelengths, columns = position
        data_matrix = data_matrix.T # rows = positions, columns = wavelengths
        
        # print(f"Successfully loaded data from {DataPfad}")
        # print(f"Number of rows (n): {data.shape[0]}")
        # print(f"Number of columns (m): {data.shape[1]}")
        # print(f"x_values shape: {w_values.shape}")
        # print(f"data_matrix shape: {data_matrix.shape}")
        
        return w_values, data_matrix, data_matrix.shape
        
    except FileNotFoundError:
        print(f"Error: File '{DataPfad}' not found.")
        return None, None
    except ValueError as e:
        print(f"Error reading file: {e}")
        print("Make sure all values are valid floating-point numbers.")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

