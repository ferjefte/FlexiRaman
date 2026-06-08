# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:04:05 2026

@author: aguilafernando

This script helps to prepare coustum plots of "H_ .np": (an np array with the component spectra found) again.
Necessary information is read from "PCAinfo_ .txt"
"""

import numpy as np
import matplotlib.pyplot as plt
import os

########## change parameters here #################################################################

# FOLDER NAMES AND DIRECTORIES

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

# date = '20250717'
# date = '20250523'
# date = '20250516'
# date = '20260107'
# date = '20260505'
# date = '20260519'
# date = '20260520'
date = '20260522'

# sample = 'PS3_3'
# sample = 'CSilicon'
# sample = 'Si_F'
# sample = 'Pig_C'
sample = 'Pig01_C'
# sample = 'Volt'

# ROI = '01'
# ROI = '03'
# ROI = '02'
ROI = '04'

test = '01'

# subfolder = r"2026-01-13_13-54-50_c5" # date = '20250523' 
# subfolder = r"2026-01-14_18-29-29_c7" # date = '20250523' 
# subfolder = r"2026-01-13_14-31-09_c5" # date = '20250516' 
# subfolder = r"2026-01-14_18-36-19_c7" # date = '20250516' 
# subfolder = r"2026-01-15_11-36-33_c5" # date = '20250717' 
# subfolder = r"2026-01-14_17-01-26_c7" # date = '20250717' 
# subfolder = r"2026-01-13_12-00-38_c3" # date = '20260107' 
# subfolder = r"2026-01-13_11-12-08_c5" # date = '20260107' 
# subfolder = r"2026-06-01_14-16-59_c6" # date = '20260107'  
# subfolder = r"2026-01-14_18-48-46_c7" # date = '20260107' 
# subfolder = r"2026-05-13_14-12-38_c5" # date = '20260505' 
# subfolder = r"2026-05-21_15-49-05_c5" # date = '20260519' 
# subfolder = '2026-06-01_14-05-38_c6' # date = '20260519
# subfolder = r"2026-05-26_16-53-46_c5" # date = '20260520' 
# subfolder = r'2026-06-01_13-52-10_c6' # date = '20260520'
subfolder = r'2026-06-01_13-21-59_c6' # date = '20260522'


# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

Pfad = working_directory


PfadPCA = Pfad +"\\PCA"
Bildpfad = PfadPCA + "\\"+ subfolder
subBildpfad = Bildpfad + "\\W" 

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
########## read Raman spectral channel #######################################################

HH=np.load(Bildpfad+"\\H"+".npy")

# plotting
colors = ['r', 'g', 'b', 'y', 'm', 'c', 'tab:orange', 'tab:brown'] # og convention (red=lipids, green=proteins, blue=whatever) 
# colors = ['b', 'r', 'g', 'y', 'm', 'c', 'tab:orange', 'tab:brown'] # for 20250523_Pig01_C_ROI03_test01

shift = 0.4

fig, ax = plt.subplots(1)
fig.set_size_inches(8, 5)

# # regular plot
# for i in range(0,n_comp):
#     ax.plot(scale_cm1[firstchannel:lastchannel+1],HH[i], label=f"comp. {i}",linewidth=1, color=colors[i])
#     plt.axhline(y=0, color='gray', linestyle=':')  # Black dotted line

# shifted plot

for i in range(0,n_comp):
    shifted_plot = np.abs(HH[i]+shift*i)
    ax.plot(scale_cm1[firstchannel:lastchannel+1],shifted_plot, label=f"comp. {i}",linewidth=1, color=colors[i])
    plt.axhline(y=0+shift*i, color='gray', linestyle=':')  # Black dotted line
    
# # plot set for 20250523_Pig01_C_ROI03_test01
# blue_plot = HH[0]
# green_plot = HH[2]
# red_plot = HH[1]
# ax.plot(scale_cm1[firstchannel:lastchannel+1], blue_plot+4*0, label=f"comp. {0}",linewidth=1, color=colors[0]) # blue
# plt.axhline(y=0, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], green_plot+4*1, label=f"comp. {1}",linewidth=1, color=colors[2]) # green
# plt.axhline(y=np.min(green_plot)+4*1, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], red_plot+4*2, label=f"comp. {2}",linewidth=1, color=colors[1]) # red
# plt.axhline(y=np.min(red_plot)+4*2, color='gray', linestyle=':')  # Black dotted line

# # plot set for 20250516_Pig01_C_ROI02_test01
# blue_plot = HH[2]
# green_plot = HH[1]
# red_plot = HH[0]
# ax.plot(scale_cm1[firstchannel:lastchannel+1], blue_plot+4*0, label=f"comp. {0}",linewidth=1, color=colors[0]) # blue
# plt.axhline(y=0, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], green_plot+4*1, label=f"comp. {1}",linewidth=1, color=colors[2]) # green
# plt.axhline(y=np.min(green_plot)+4*1, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], red_plot+4*2, label=f"comp. {2}",linewidth=1, color=colors[1]) # red
# plt.axhline(y=np.min(red_plot)+4*2, color='gray', linestyle=':')  # Black dotted line

# # plot set for 20250717_PS3_3_ROI03_test01
# blue_plot = HH[1]
# green_plot = HH[0]
# red_plot = HH[2]
# ax.plot(scale_cm1[firstchannel:lastchannel+1], blue_plot+4*0, label=f"comp. {0}",linewidth=1, color=colors[0]) # blue
# plt.axhline(y=0, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], green_plot+4*1, label=f"comp. {1}",linewidth=1, color=colors[2]) # green
# plt.axhline(y=np.min(green_plot)+4*1, color='gray', linestyle=':')  # Black dotted line
# ax.plot(scale_cm1[firstchannel:lastchannel+1], red_plot+4*2, label=f"comp. {2}",linewidth=1, color=colors[1]) # red
# plt.axhline(y=np.min(red_plot)+4*2, color='gray', linestyle=':')  # Black dotted line

plt.legend(bbox_to_anchor=(1.17, 1), loc='upper right', borderaxespad=0)
plt.xlabel("Wavenumber [$cm^{-1}$]")
plt.ylabel("Intensity [arb.]")
plt.yticks([])
plt.title(f"PCA components for {folder_name}")
#plt.xlim(700, 1300)
plt.xlim(270, 3830)
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig(Bildpfad+"\\PCA_H_plot"+f"_{n_comp}c_{folder_name}.png", format="png", dpi=300)
# plt.close()

# #%%
# # ZOOM TO specific REGION

# # index corresponding to the value where you wanna truncate the plot
# # wn_v_r = 1796
# # wn_v_l = 0
# wn_v_r = 3446 # ps-pmma
# wn_v_l = 2635 # ps-pmma
# # wn_v_r = 3667  # pig
# # wn_v_l = 2618  # pig
# idx_r = np.argmin(np.abs(scale_cm1-wn_v_r))
# idx_l = np.argmin(np.abs(scale_cm1-wn_v_l))
# wn_r = np.round(scale_cm1[idx_r], 2)
# wn_l = np.round(scale_cm1[idx_l], 2)

# fig, ax = plt.subplots(1)
# fig.set_size_inches(7, 6)

# for i in range(0,n_comp):
#     HH_p = HH[i][idx_l:idx_r] 
#     ax.plot(scale_cm1[idx_l:idx_r],HH_p+shift*i, label=f"comp. {i}",linewidth=1, color=colors[i])
#     plt.axhline(y=0+shift*i, color='gray', linestyle=':')  # Black dotted line

# plt.legend(bbox_to_anchor=(1.2, 1), loc='upper right', borderaxespad=0)
# plt.xlabel("Wavenumber [$cm^{-1}$]")
# plt.ylabel("Intensity [arb.]")
# plt.yticks([])
# plt.title(f"PCA components for {folder_name} \n region {wn_l} to {wn_r} 1/cm")
# plt.grid()
# plt.tight_layout()
# plt.show()
# plt.savefig(Bildpfad+"\\PCA_H_plot"+f"_{n_comp}c_{folder_name}_region{round(wn_r)}.png", format="png", dpi=300)