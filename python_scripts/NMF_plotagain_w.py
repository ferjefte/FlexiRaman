# -*- coding: utf-8 -*-
"""
Created on Wed May 21 14:15:21 2025

@author: hauswaldwalter

This script helts to prepare coustum plots of "H_ .np": (an np array with the component spectra found) again.
Necessary information is read from "NMFinfo_ .txt"
"""

import numpy as np
import matplotlib.pyplot as plt

########## change parameters here #################################################################

Pfad = r"E:\MultiHoloDiag\AP31_GrundlegendeVoruntersuchungen_WalterLydia\Versuchsreihe 19\20211027 MHD VR19 Laser"
Pfad = r"E:\FlexiRaman\2025-05-07 Schweinehaut"
Pfad = r"F:\flexiRaman\20250226_PS3_3_ROI01_test01"
subfolder = r"2025-07-24_15-35-41_c7"
jj = 199
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
scale_cm1 = scale_cm1=10000000/ui_LaserWL-10000000/scale
########## read Raman spectral channel #######################################################

HH=np.load(Bildpfad+"\\H_jj"+str(jj).zfill(5)+".npy")

# plotting
fig, ax = plt.subplots(1)
fig.set_size_inches(8, 5)
for i in range(0,n_comp):
    ax.plot(scale_cm1[firstchannel:lastchannel+1],HH[i], label=f"comp. {i}",linewidth=1)

plt.legend()
plt.xlabel("Wavenumber $/cm^{-1}$")
plt.ylabel("Intensity /arb.")
plt.title(str(n_comp) + " component spectra obtained with NMF")
#plt.xlim(700, 1300)
plt.xlim(0, 4000)
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig(Bildpfad+"\\H_plot_jj"+str(jj).zfill(5)+"n.png", format="png", dpi=300)
plt.close()