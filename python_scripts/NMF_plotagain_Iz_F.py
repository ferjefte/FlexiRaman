# -*- coding: utf-8 -*-
"""
Created on Wed May 21 14:15:21 2025

@author: hauswaldwalter

This script helts to prepare coustum plots of "H_ .np": (an np array with the component spectra found) again.
Necessary information is read from "NMFinfo_ .txt"
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

########## change parameters here #################################################################

# FOLDER NAMES AND DIRECTORIES

project_directory = Path(__file__).parent.parent
data_directory = os.path.join(project_directory, "data")



# date = '20260107'
# date = '20260505'
date = '20260513'

sample = 'PS3_3'

# sample = 'Pig01_C'


# ROI = '01'
# ROI = '03'
ROI = '02'

# test = '01'
test = '02'


# subfolder = r"2025-08-12_13-25-28_c5" # date = '20260505' five
# subfolder = r"2026-05-12_15-48-30_c7" # date = '20260505' seven
subfolder = r"2026-05-19_17-37-21_c7" # date = '20260513' seven




# RAW MEASUREMENTS DIRECTORY
folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)

Pfad = working_directory

# jj = 199 # date = '20250717'
# jj= 184 # of 5 comp on 20250516
jj = 169 # seven comp. 
# jj = 88 # date = '20260107'
# jj = 159 # date = '20260107' seven comp.
PfadNMF = Pfad +"\\NMF"
Bildpfad = PfadNMF + "\\"+ subfolder
subBildpfad = Bildpfad + "\\W_jj" + str(jj).zfill(5)

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
# scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale
########## read Raman spectral channel #######################################################

HH=np.load(Bildpfad+"\\H_jj"+str(jj).zfill(5)+".npy")

# plotting
colors = ['r', 'g', 'b', 'y', 'm', 'c', 'tab:orange', 'tab:brown'] # og convention (red=lipids, green=proteins, blue=whatever) 
# colors = ['b', 'r', 'g', 'y', 'm', 'c', 'tab:orange', 'tab:brown'] # for 20250523_Pig01_C_ROI03_test01

shift = 4

fig, ax = plt.subplots(1)
fig.set_size_inches(8, 5)

for i in range(0,n_comp):
    ax.plot(scale[firstchannel:lastchannel+1],HH[i]+shift*i, label=f"comp. {i}",linewidth=1, color=colors[i])
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
plt.title(f"NMF components for {folder_name}")
#plt.xlim(700, 1300)
plt.xlim(270, 3830)
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig(Bildpfad+"\\NMF_H_plot_jj"+str(jj).zfill(5)+f"_{n_comp}c_{folder_name}.png", format="png", dpi=300)
# plt.close()

#%%
# ZOOM TO specific REGION

# index corresponding to the value where you wanna truncate the plot
# wn_v_r = 1796
# wn_v_l = 0
# wn_v_r = 3667 # pig
# wn_v_l = 2618 # pig
wn_v_r = 3100 # pig
wn_v_l = 2500 # pig
idx_r = np.argmin(np.abs(scale-wn_v_r))
idx_l = np.argmin(np.abs(scale-wn_v_l))
wn_r = np.round(scale[idx_r], 2)
wn_l = np.round(scale[idx_l], 2)

fig, ax = plt.subplots(1)
fig.set_size_inches(7, 6)

for i in range(0,n_comp):
    HH_p = HH[i][idx_l:idx_r] 
    ax.plot(scale[idx_l:idx_r],HH_p+shift*i, label=f"comp. {i}",linewidth=1, color=colors[i])
    plt.axhline(y=0+shift*i, color='gray', linestyle=':')  # Black dotted line

plt.legend(bbox_to_anchor=(1.2, 1), loc='upper right', borderaxespad=0)
plt.xlabel("Wavenumber [$cm^{-1}$]")
plt.ylabel("Intensity [arb.]")
plt.yticks([])
plt.title(f"NMF components for {folder_name} \n region {wn_l} to {wn_r} 1/cm")
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig(Bildpfad+"\\NMF_H_plot_jj"+str(jj).zfill(5)+f"_{n_comp}c_{folder_name}_region{round(wn_r)}.png", format="png", dpi=300)
