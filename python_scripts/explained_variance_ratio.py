# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:50:12 2026

Script to plot the explained variance ratio and calculate the cumulative variance

@author: aguilafernando
"""

import os
import numpy as np
import matplotlib.pyplot as plt

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

# date = '20260107'
# date = '20260505'
# date = '20260513'
# date = '20260519'
# date = '20260520'
date = '20260522'


sample = 'Pig01_C'
# sample = 'PS3_3'

# roi = '03'
# roi = '02'
# roi = '01'
roi = '04'


test = '01'
# test = '02'

folder_name = date+"_"+sample+"_ROI"+roi+"_test"+test

folder_name_path = os.path.join(project_directory, folder_name)

pca_folder_path = os.path.join(folder_name_path, 'PCA')

# pca_folder_name = '2026-01-13_11-12-08_c5' # for date = '20260107'
# pca_folder_name = '2026-06-01_14-16-59_c6' # for date = '20260107'
# pca_folder_name = '2026-05-13_14-26-05_c5' # for date = '20260505'
# pca_folder_name = '2026-06-01_14-34-28_c6' # for date = '20260505'
# pca_folder_name = '2026-05-19_15-48-30_c5' # for date = '20260513'
# pca_folder_name = '2026-06-01_14-29-58_c6' # for date = '20260513'
# pca_folder_name = '2026-05-21_15-49-05_c5' # for date = '20260519'
# pca_folder_name = '2026-06-01_14-05-38_c6' # for date = '20260519'
# pca_folder_name = '2026-05-26_16-53-46_c5' # for date = '20260520'
# pca_folder_name = '2026-06-01_13-52-10_c6' # for date = '20260520'
# pca_folder_name = '2026-05-26_17-34-48_c5' # for date = '20260522'
pca_folder_name = '2026-06-01_13-21-59_c6' # for date = '20260522


working_directory = os.path.join(pca_folder_path, pca_folder_name)

pcares_path = os.path.join(working_directory, 'PCAres.txt')

#%% READ DATA FROM PCAres.txt file

try:
    data = np.loadtxt(pcares_path, delimiter=',', skiprows=1)
    explained_variance_ratio = data[:, 1]  # Second column (index 1)
    
    print("Explained Variance Ratio for each component:")
    for i, ratio in enumerate(explained_variance_ratio, 1):
        print(f"PC{i}: {ratio:.4f} ({ratio*100:.2f}%)")
    
    # Calculate cumulative variance
    cumulative = np.cumsum(explained_variance_ratio)
    print("\nCumulative Variance Ratio:")
    for i, cum in enumerate(cumulative, 1):
        print(f"After PC{i}: {cum:.4f} ({cum*100:.2f}%)")

except Exception as e:
    print(f"Error reading file: {e}")
    
# save the explained variance ratio array
results_directory = os.path.join(project_directory, 'data_presentation')
evr_filepath = os.path.join(results_directory, f'expl_variance_ratio_{sample}_{date}')
cum_filepath = os.path.join(results_directory, f'cum_variance_{sample}_{date}')
np.save(evr_filepath, explained_variance_ratio)
np.save(cum_filepath, cumulative)
#%% PLOTTING

num_comp = np.arange(1,len(explained_variance_ratio)+1,1 )

fig, ax = plt.subplots(1,1)

ax.plot(num_comp, explained_variance_ratio*100, 'o--')
ax.set_xticks(num_comp)
ax.set_xlabel('PCA-component')
ax.set_ylabel('Variance ratio [%]')
ax.set_title(f'Explained variance ratio for sample {sample}_{date}')
# plt.savefig(working_directory+"/VR_plot.png", format="png", dpi=300)


#%% PLOTTING ALL TOGETHER

# couting number of files with search_string in results_directory
search_string = sample
files = [f for f in os.listdir(results_directory)
         if  f.endswith('.npy') and search_string in f]

title_name = files[0].split('_')[2].split('.')[0]

colors = ['r', 'g', 'b', 'y']

fig, ax = plt.subplots(1,1)
for i,f in enumerate(files):
    f_evr = np.load(os.path.join(results_directory, f))
    x = np.arange(1,len(f_evr)+1)
    name_start = f.split('_')[0]
    name = f.split('_')[-1].split('.')[0]
    if name == '20260505' or name == '20260513':
        name = name + '_Izabella'
    if name == '20260107' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[1])
    elif name == '20260107' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[1])
    elif name == '20260505_Izabella' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[0])
    elif name == '20260505_Izabella' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[0])
    elif name == '20260513_Izabella' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[2])
    elif name == '20260513_Izabella' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[2])
    elif name == '20260519' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[0])
    elif name == '20260519' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[0])
    elif name == '20260520' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[1])
    elif name == '20260520' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[1])
    elif name == '20260522' and name_start == 'cum':
        ax.plot(x, f_evr*100, 'o--', label=name, color=colors[2])
    elif name == '20260522' and name_start == 'expl':
        ax.plot(x, f_evr*100, 'o--', color=colors[2])
    else:        
        ax.plot(x, f_evr*100, 'o--', label=name)
    ax.set_xticks(x)
ax.set_title(f'Explained variance ratio/Cumulative variance for {title_name}')
ax.set_xlabel('Component')
ax.set_ylabel('[%]')
ax.legend()

plt.savefig(results_directory+f"/VR_{title_name}_comparison_plot.png", format="png", dpi=300)