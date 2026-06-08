#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:16:24 2024

PROGRAM FOR THE PROCESSING OF THE RAW DATA IMAGES FROM THE NEON SPECTRUM
MISSING AND EXTRA PIXELS FROM THE SPECTRAL LINES ARE ADDED OR ERRASED RESPECTIVELEY 
RESULT IS THE NUMPY FILE AND/OR THE MATLAB FILE WITH THE MASK THAT IS USED FOR THE CALCULATION OF THE CENTER OF MASS

@author: fernandoaguila
"""

import numpy as np
import matplotlib.pylab as plt
import os
import scipy.ndimage as ndimage
from mask import mask_maker
from img_dark_processor import img_dark_pross
import tifffile as tf
from calibration_raw_img_process import img_load_avg


# FILE NAMES AND DIRECTORIES
project_directory = r'D:\Projekte\Flexiraman\Fernando'

date = '20240906'
# date = '20250514'
# date = '20251029'
# date = '20260105'
date = '20260106'

sample = 'Neon_lamp'

test = '01'

folder_name =  date+'_'+sample+'_test'+test


working_directory = os.path.join(project_directory, folder_name)


data_directory = os.path.join(working_directory, 'calibration_data')


#%%
# LOADING AND AVERAGING OF IMAGES 
img_load_avg(working_directory)

#%%
# LOADING OF RAW AVERAGE NEON SPECTRUM IMAGES
img_hi_nof = np.load(data_directory+'/img_hi_nof.npy')
img_hi_dark_nof = np.load(data_directory+'/img_hi_dark_nof.npy')
img_hi_yesf = np.load(data_directory+'/img_hi_yesf.npy')
img_hi_dark_yesf = np.load(data_directory+'/img_hi_dark_yesf.npy')

# # CASE WHEN LP FILTER AND BP FILTER ARE USED
# img_hi_yesf_g = np.load(data_directory+'/img_hi_yesf_g.npy')
# img_hi_dark_yesf_g = np.load(data_directory+'/img_hi_dark_yesf_g.npy')
# img_hi_yesf = img_hi_yesf+img_hi_yesf_g

# img_hi_dark_yesf = img_hi_dark_yesf+img_hi_dark_yesf_g

# fig, ax=plt.subplots(1,1)
# ax.set_title('gaussian_filtered_image without BP filter')
# ax.imshow(img_hi_yesf_g, cmap='gray_r', vmin=0, vmax=300)





#%%
# DARK BACKGROUND CORRECTION 
img_hi, img_hi_nof_c, img_hi_yesf_c = img_dark_pross(img_hi_nof, img_hi_dark_nof, 
                                                     img_hi_yesf, img_hi_dark_yesf, 
                                                     'img_corrected', 'img_nof_corrected', 
                                                     'img_yesf_corrected', 
                                                     data_directory)

# # IN CASE OF LOADING
# img_hi_nof_c = np.load(data_directory+'\\img_nof_corrected.npy')
# img_hi_yesf_c = np.load(data_directory+'\\img_yesf_corrected.npy')
# img_hi = np.load(data_directory+'\\img_corrected.npy')

# VISUALISATION 
# fig, ax=plt.subplots(1,1)
# ax.set_title('dark_current_correction')
# ax.imshow(img_hi_yesf_c, cmap='gray_r', vmin=0, vmax=50)

# fig, ax=plt.subplots(1,1)
# ax.imshow(img_hi, cmap='gray_r', vmin=0, vmax=1000)
# fig.savefig('neon_speclines_flexiraman_slit20230803.jpg', dpi=400)

img_hi_processed = img_hi

# # GAUSS FILTER
# img_hi_processed=ndimage.gaussian_filter(img_hi, sigma=1.3)
# img_hi_nof_c=ndimage.gaussian_filter(img_hi_nof_c, sigma=1.3)
# img_hi_yesf_c=ndimage.gaussian_filter(img_hi_yesf_c, sigma=1.3)

# MEDIAN FILTER
# img_hi=ndimage.median_filter(img_hi, size=(3,3))
# img_hi_nof_c=ndimage.median_filter(img_hi_nof_c, size=(3,3))
# img_hi_yesf_c=ndimage.median_filter(img_hi_yesf_c, size=(3,3))

### VISUALISATION

fig, ax=plt.subplots(1,1)
ax.set_title('no_filter')
ax.imshow(img_hi_nof_c, cmap='gray_r', vmin=0, vmax=300)

fig, ax=plt.subplots(1,1)
ax.set_title('yes_filter')
ax.imshow(img_hi_yesf_c, cmap='gray_r', vmin=100, vmax=2000)

fig, ax=plt.subplots(1,1)
ax.set_title('combined')
# img_mask=img_hi_nof_c+img_hi_yesf_c
ax.imshow(img_hi_processed, cmap='gray_r', vmin=0, vmax=2000)


#%%
### CALCULATING MASK
mask, mask_dialated = mask_maker(img_hi_yesf_c, img_hi_nof_c, man_thresh_filter=200,  man_thresh_nofilter=150 )

### VISUALISATION 

#%%
fig, ax=plt.subplots(1,1)
ax.set_title('mask_dialated')
ax.imshow(mask_dialated)

#%%
fig, ax=plt.subplots(1,1)
ax.set_title('mask')
ax.imshow(mask)

#%% 
# ### APERTURE ADJUSTMENT FOR SLIT MASK C4 ON 06/09/2024 MEASUREMENT

# # threshold values: with filter=140, without filter=150
# ### ADDED
# mask_dialated[1670:1677,436:438]=True
# mask_dialated[1810:1816,440:442]=True
# mask_dialated[1996:2002,446:448]=True

#%%
### APETURE ADJUSTMEN FOR SLIT MASK C4 ON 29/08/2024 MEASUREMENT

# threshold values: with filter=40, without filter=50

### ADDED
# mask_dialated[1994:1999,690:696]=True
# mask_dialated[1671:1676,436:438]=True
# mask_dialated[1810:1816,440:442]=True
# mask_dialated[1996:2002,446:448]=True

# ### ELIMINATED
# mask_dialated[1478:1483,960:965]=False
# mask_dialated[183:186, 179:182]=False
# mask_dialated[648:651,657:660]=False

#%%
# ### APETURE ADJUSTMEN FOR SLIT MASK C4 ON 16/08/2024 MEASUREMENT

# ### ADDED
# mask_dialated[1812:1817,690:695]=True
# mask_dialated[1994:2003,2046:2048]=True
# mask_dialated[1582:1587,440:441]=True
# mask_dialated[1768:1774,445:446]=True
# mask_dialated[1861:1867,448:449]=True

# ### ELIMINATED

# mask_dialated[45:51,0:5]=False
# mask_dialated[92:97,0:5]=False
# mask_dialated[140:144,0:3]=False
# mask_dialated[187:191,184:188]=False
# mask_dialated[327:331,181:185]=False
# mask_dialated[334:339,1148:1153]=False
# mask_dialated[420:424,181:184]=False
# mask_dialated[420:424,240:244]=False
# mask_dialated[607:611,178:182]=False
# mask_dialated[651:656,661:665]=False
# mask_dialated[1727:1731,2:7]=False
# mask_dialated[1290:1295,1560:1563]=False


#%%
### ADJUSTMEN OF LOST PIXELS FOR SLIT MASK 20230803

### ADDED

## for cpos0 case

# mask_dialated[576:1348,174:280]=False
# mask_dialated[1666:1675,34:45]=False
# mask_dialated[317:323,1325:1331]=False

## for cposm1 case

# mask_dialated[1785:2040,150:173]=False
# mask_dialated[500:513,1007:1023]=False
# mask_dialated[1564:1572,1352:1360]=False
# mask_dialated[1769:1780,1608:1625]=False
# mask_dialated[1780:1786,1615:1625]=False
# mask_dialated[112:121,542:550]=False
# mask_dialated[878:888,747:760]=False
# mask_dialated[1000:1008,1836:1844]=False
# mask_dialated[468:476,1683:1691]=False
# mask_dialated[1364:1370,434:440]=False

# mask_dialated[863:869,697:703]=True
# mask_dialated[956:963,694:702]=True
# mask_dialated[1096:1100,694:699]=True
# mask_dialated[1003:1010,695:701]=True
# mask_dialated[1140:1150,692:702]=True
# mask_dialated[1187:1195,692:700]=True
# mask_dialated[1232:1242,695:703]=True
# mask_dialated[1279:1288,690:700]=True
# mask_dialated[1325:1335,693:703]=True
# mask_dialated[1374:1381,690:699]=True
# mask_dialated[1418:1429,692:701]=True
# mask_dialated[1465:1473,692:701]=True
# mask_dialated[1508:1518,692:702]=True
# mask_dialated[1558:1566,692:700]=True
# mask_dialated[1606:1614,692:702]=True
# mask_dialated[1655:1660,692:701]=True
# mask_dialated[1698:1705,694:702]=True
# mask_dialated[1746:1752,694:701]=True
# mask_dialated[1787:1797,695:707]=True
# mask_dialated[1834:1843,696:707]=True
# mask_dialated[1884:1891,696:706]=True
# mask_dialated[1928:1937,696:707]=True
# mask_dialated[1975:1984,702:707]=True

## for cposp1

# mask_dialated[1996:2001,266:271]=False
# mask_dialated[380:420,200:290]=False
# mask_dialated[632:638,340:346]=False
# mask_dialated[1456:1464,502:512]=False
# mask_dialated[1716:1722,570:576]=False
# mask_dialated[84:93,862:870]=False
# mask_dialated[1091:1098,1252:1258]=False

# # mask_dialated[25:30,725:730]=True
# # mask_dialated[118:124,720:726]=True
# # mask_dialated[165:170,718:725]=True

## for cposp2

# mask_dialated[1048:1052,1172:1176]=False

# mask_dialated[1935:1943,125:139]=True
# mask_dialated[1983:1989,129:138]=True
# mask_dialated[261:269,715:724]=True
# mask_dialated[354:362,712:720]=True
# mask_dialated[446:455,708:717]=True
# mask_dialated[538:547,706:714]=True

# # mask_dialated[1933:1936,702:706]=True
# # mask_dialated[1980:1983,704:707]=True
# # mask_dialated[1941:1944,132:136]=True
# # mask_dialated[1988:1991,133:137]=True

## caser for posp1

# # mask_dialated[1933:1936,702:706]=True
# # mask_dialated[1980:1983,704:707]=True
# # mask_dialated[1941:1944,132:136]=True
# # mask_dialated[1988:1991,133:137]=True
# # mask_dialated[27:33,727:732]=True
# # mask_dialated[120:127,722:729]=True

## case for posm2

# mask_dialated[75:80, 725:731]=True
# mask_dialated[167:173, 721:726]=True
# mask_dialated[214:220, 719:725]=True
# mask_dialated[258:267, 716:722]=True
# mask_dialated[306:313, 715:721]=True
# mask_dialated[352:359, 713:720]=True
# mask_dialated[398:406, 711:718]=True
# mask_dialated[444:453, 710:716]=True
# mask_dialated[491:500, 708:716]=True
# mask_dialated[537:546, 706:715]=True
# mask_dialated[26:32, 724:732]=True
# mask_dialated[118:124, 721:727]=True


### DELETED

# # mask_dialated[115:119,238:243]=False
# # mask_dialated[1975:2000,50:270]=False
# # mask_dialated[1975:2000,950:965]=False
# # mask_dialated[1426:1432,954:960]=False
# # mask_dialated[805:813,1260:1272]=False
# # mask_dialated[1188:2000,640:700]=False
# # mask_dialated[710:720,240:250]=False

# # mask_dialated[483:1434, 189:284]=False
# # mask_dialated[1052:1056, 346:351]=False
# # mask_dialated[1048:1052, 1173:1177]=False
# # mask_dialated[1051:1053, 1173:1177]=False

## caser for posp1

# # mask_dialated[1045:1198, 689:694]=False
# # mask_dialated[1276:1802, 689:693]=False
# # mask_dialated[1802:1992, 690:696]=False

#%% 
### APERTURE ADJUSTMENT FOR SLIT MASK B1 (FR2022_4) ON 06/01/2026 MEASUREMENT

# threshold values: with filter=200, without filter=150
# ### ELIMINATED
mask_dialated[294:300,100:106]=False
mask_dialated[434:534, 96:108]=False
mask_dialated[666:860,94:105]=False
mask_dialated[991:1188,96:108]=False
mask_dialated[1274:1279,101:107]=False
mask_dialated[1414:1419,104:108]=False
mask_dialated[1741:1746,111:117]=False
mask_dialated[1974:1979,116:122]=False

mask_dialated[54:2040,400:456]=False

mask_dialated[527:531,665:670]=False
mask_dialated[617:1276,661:675]=False
mask_dialated[1407:1694,670:683]=False

#%%
### VISUALISATION 

mask_name = "mask_dilated"+folder_name
mask_path = os.path.join(data_directory, mask_name)


fig, ax=plt.subplots(1,1)
# ax.set_title('mask_dialated')
ax.imshow(mask_dialated, cmap='gray_r', vmin=0, vmax=1)

ax.set_xlabel('Pixel number')
ax.set_ylabel('Pixe number')
# ax.set_ylabel('Slit position [mm]')

fig.savefig(mask_path, dpi=300)
#%%
fig, ax=plt.subplots(1,1)
ax.set_title('mask')
ax.imshow(mask, cmap='gray_r', vmin=0, vmax=1)
#%%
### FINAL IMAGE USED FOR CENTER OF MASSS CALCULATIONS

img_centermass=mask_dialated*img_hi_processed

#%%
### SAVING PYHTON FILE 
img_centermass_path = os.path.join(data_directory, 'img_centermass')
np.save(img_centermass_path, img_centermass)

# SAVING NUMPY FILES OF EXPANDED HOLES MASK AND PROCESSED IMAGE
mask_dialated_path = os.path.join(data_directory, 'mask_expand')
np.save(mask_dialated_path, mask_dialated)

img_hi_processed_path = os.path.join(data_directory, 'img_hi_processed')
np.save(img_hi_processed_path, img_hi_processed)

### SAVING PROCESSED SPECTRAL IMAGE FILE
processed_spectral_image_path = os.path.join(data_directory, 'processsed_spectrum.tif')
tf.imwrite(processed_spectral_image_path, np.uint32(img_hi_processed))
