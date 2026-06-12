# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 13:41:10 2025

@author: hauswaldwalter
"""
import numpy as np
#import tifffile as tf

#####################################################################################################################
def linear2srgb(img, inMin=0.0, inMax=65535.0, outType=np.uint8):
    """Konvertiert ein lineares RGB-Bild in sRGB. (intern np.float32)
        inverse OETF as defined in the IEC standard is not used for EOTF
        https://en.wikipedia.org/wiki/SRGB
    
    Args:
      img: Ein NumPy-Array mit Form z.B. (height, width) oder (height, width, 3) und Werten zwischen inMin und inMax.
      inMin=0.0: minimum input level (to be projected to outMin), typ: cammera dark level or a little higher
      inMax=65535.0: maximum input level (to be projected to outMin), typ: level of brightest region of image
      outType=np.uint8: np.uint8 or np.uint16
    
    Returns:
      Ein NumPy-Array mit Form (height, width, 3) und Werten zwischen 0 und outMax (outType).
    """
    if (outType==np.uint8):
        outMax=255
    elif (outType==np.uint16):
        outMax=65535
    elif (outType==np.float32):
        outMax=1.0
    else:
        return "wrong outType"

    img = (img.astype(np.float32) - inMin) / (inMax - inMin)  # Normalisieren auf 0.0 - 1.0
    img = np.maximum(img,0) # damit der np.power Befehl keine Fehler erzeugt und nach unten abgeschnitten wird
    img = np.where(img <= 0.0031308, img * 12.92, 1.055 * np.power(img, 1.0 / 2.4) - 0.055) # Transfer function
    img = np.minimum(img,1) # damit nach oben abgeschnitten wird
    #img = np.clip(img, 0.0, 1.0) # alt funktioniert aber weder vor noch nach der Transfer function fehlerfrei
    return (img * outMax).astype(outType)

#####################################################################################################################
def contrastGamma (img,inMin,inMax,outMin,outMax,gamma):
    """Konvertiert ein lineares RGB-Bild in ein gamma Bild (intern np.float32)
    
    Args:
        #img:    input image Ein NumPy-Array mit Form z.B. (height, width) oder (height, width, 3) und Werten zwischen inMin und inMax.
        #inMin:   minimum input level (to be projected to outMin), typ: cammera dark level or a little higher
        #inMax:   maximum input level (to be projected to outMin), typ: level of brightest region of image
        #outMin:  typ: 0
        #outMax:  typ: 255 or 65535
        #gamma:    use 1 to gain a linear result, use 1/2.2 to compensate for monitor gamma of 2.2
        
    Returns:
      Ein NumPy-Array np.float32 mit Form (height, width, 3) und Werten zwischen outMin und outMax.
    """
    
    if (gamma == 1):
        return (np.clip((img.astype(np.float32)-inMin)/(inMax-inMin),0,1))*(outMax-outMin)+outMin # viel Zeit braucht np.clip !!!
    else:
        return (np.clip((img.astype(np.float32)-inMin)/(inMax-inMin),0,1)**gamma)*(outMax-outMin)+outMin # viel Zeit brauchen **gamma und np.clip !!!
    #https://numpy.org/devdocs/user/quickstart.html
    #https://stackoverflow.com/questions/14448763/is-there-a-convenient-way-to-apply-a-lookup-table-to-a-large-array-in-numpy

#####################################################################################################################
def levelsIO (img,inMin,inMax,outMin,outMax):
    """Konvertiert ein lineares RGB-Bild in ein gamma Bild (intern np.float32)
    
    Args:
        #img:    input image Ein NumPy-Array mit Form z.B. (height, width) oder (height, width, 3) und Werten zwischen inMin und inMax.
        #inMin:   minimum input level (to be projected to outMin), typ: cammera dark level or a little higher
        #inMax:   maximum input level (to be projected to outMin), typ: level of brightest region of image
        #outMin:  typ: 0
        #outMax:  typ: 255 or 65535
        
    Returns:
      Ein NumPy-Array np.float32 mit Form (height, width, 3) und Werten zwischen outMin und outMax.
    """
    
    return (np.clip((img.astype(np.float32)-inMin)/(inMax-inMin),0,1))*(outMax-outMin)+outMin # viel Zeit braucht np.clip !!!

#####################################################################################################################
def levelsI (img, inMin=0.0, inMax=65535.0, outType=np.uint8):
    """Konvertiert ein lineares RGB-Bild in ein gamma Bild (intern np.float32)
    
    Args:
        #img:    input image Ein NumPy-Array mit Form z.B. (height, width) oder (height, width, 3) und Werten zwischen inMin und inMax.
        #inMin:   minimum input level (to be projected to outMin), typ: cammera dark level or a little higher
        #inMax:   maximum input level (to be projected to outMin), typ: level of brightest region of image
        #outMin:  typ: 0
        #outMax:  typ: 255 or 65535
        
    Returns:
      Ein NumPy-Array np.float32 mit Form (height, width, 3) und Werten zwischen outMin und outMax.
    """
    if (outType==np.uint8):
        outMax=255
    elif (outType==np.uint16):
        outMax=65535
    else:
        return "wrong outType"
    
    img = (img.astype(np.float32) - inMin) / (inMax - inMin)  # Normalisieren auf 0.0 - 1.0
    img = np.clip(img, 0.0, 1.0) # viel Zeit braucht np.clip !!!
    return (img * outMax).astype(outType)

#####################################################################################################################
# # Bildgröße
# height = 1024
# width = 1024

# # Erstelle ein leeres 16-Bit-Array für das RGB-Bild
# image_16bit = np.zeros((height, width, 3), dtype=np.uint16)

# # Erzeuge den Farbverlauf
# for y in range(height):
#   for x in range(width):
#     # Berechne den Farbwert basierend auf der horizontalen Position
#     gradient_value = int(x / width * 65535)  # Skaliere auf den Bereich 0-65535

#     # Setze die RGB-Werte
#     image_16bit[y, x, 0] = gradient_value  # Rot
#     image_16bit[y, x, 1] = gradient_value  # Grün
#     image_16bit[y, x, 2] = gradient_value  # Blau

# tf.imwrite("lin16bitGradiant.tif", image_16bit.astype('uint16'), photometric='rgb')
# rgb_img = linear2srgb(image_16bit, 65535.0, np.uint16)
# tf.imwrite("lin16bitGradiant2sRGB16.tif", rgb_img, photometric='rgb')
# tf.imwrite("lin16bitGradiant2Gamma0-45.tif", ContrastGamma(image_16bit,0,65535,0,255,0.45).astype('uint8'), photometric='rgb')
