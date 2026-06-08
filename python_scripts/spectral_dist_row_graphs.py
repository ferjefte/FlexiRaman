# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:25:13 2026
PROGRAM TO PLOT THE DISTRIBUTION OF THE SPECTRAL AT DIFFERENT SENSOR POSITIONS LINES IN A SNGLE ROW PLOT
@author: aguilaremote
"""



import matplotlib.pyplot as plt
import numpy as np
import os

#%%
# FOLDER PATHS

project_directory = r'D:\Projekte\Flexiraman\Fernando'
data_directory = r'D:\Projekte\Flexiraman\Fernando\data'

test = '01'
date = '20251029'
# date = '20240906'
# date = '20260106'
sample = 'Neon_lamp' #'CSilicon' #PS3_3



folder_name =  date+'_'+sample+'_test'+test

working_directory = os.path.join(project_directory, folder_name)
interpolation_directory = os.path.join(working_directory, 'cubic_interpolation_python')
calibration_directory = os.path.join(working_directory, 'calibration_data')
plots_directory = os.path.join(interpolation_directory, 'plots')

interpolation_file = os.path.join(interpolation_directory, 'image_0000.npy')
wavelength_file = os.path.join(calibration_directory, 'wavelengths.npy')


#%%
# DATA

# numpy array for the spectra 
interpolation = np.load(interpolation_file)

# wavelengths array
wavelen = np.load(wavelength_file)
# raman shift 
# wavelen_shift = 1e7/532 - (1e7/wavelen)

# fig, ax = plt.subplots(1,1)
# ax.imshow(interpolation, vmin=0, vmax=200, cmap='gray_r')

# Chosen lines and rows 
rows = [44, 53, 1043, 1053, 1994, 2006] # [upper_1, upper_2, mid_1, mid_2, lower_1, lower_2]

speclines_index = [256, 267, 1108, 1121, 1911, 1926] # [left_1, left_2, mid_1, mid_2, right_1, right_2]

true_wavelens = [556.28, 609.62, 659.90]

# indexes where to find the true wavelengths in wavelen array
indx_true_wln = []
for i in range(3):
    ind = np.argmin(np.abs(wavelen-true_wavelens[i]))
    indx_true_wln.append(ind)

# Claculate the avereage spectra and assign wavelength ranges
avgs = []
summs = []
row_pixels = []
single_row_spectra = []
wavelens = []
wavelens_ranges = []
for i in range(0,6,2):
    
    # single row spectra
    single_row_idx =  int( rows[i] + ( rows[i+1]-rows[i] )/2 )
    row_pixels.append(single_row_idx)
    single_row_specs = interpolation[ single_row_idx,: ] 
    single_row_spectra.append(single_row_specs)
    
    # average calculation
    avg = np.average(interpolation[rows[i]:rows[i+1],:], axis=0)
    avgs.append(avg)
    
    # sums of rows
    summ = np.sum(interpolation[rows[i]:rows[i+1],:], axis=0)
    summs.append(summ)
    
    # wavelens extraction
    wl = wavelen[speclines_index[i]:speclines_index[i+1]]
    wavelens.append(wl)
    
    # wavelen ranges calculation
    wlr = wavelen[indx_true_wln[i//2]-4: indx_true_wln[i//2]+5: 4 ]
    wavelens_ranges.append(np.round(wlr,2))
    
    
# Names and colors

names = ['upper', 'middle', 'bottom']
names_single = [str(i) for i in row_pixels]
names_several = [str(rows[i])+'--'+str(rows[i+1]) for i in range(0,6,2)]
colors = ['red', 'green', 'blue']
#%%
# PLOTTING

# Create a figure and a set of subplots with shared x-axis and no vertical spacing
fig, ax = plt.subplots(1, 3, figsize=(7,5), sharey='row', sharex='col', gridspec_kw={'hspace': 0, 'wspace': 0.02})
for i in range(0,6,2):
        
    
    for j in range(3):
        # # averages plot
        # ax[i//2].plot( wavelens[j], avgs[j][speclines_index[i]:speclines_index[i+1]], label='pixel rows: '+names_single[j], color=colors[j], marker='.' )

        # summs plot
        ax[i//2].plot( wavelens[i//2], summs[j][speclines_index[i]:speclines_index[i+1]], label='pixel rows:'+names_several[j], color=colors[j], marker='.' )

        # single row spectra 
        # ax[i//2].plot( wavelens[i//2], single_row_spectra[j][speclines_index[i]:speclines_index[i+1]], label='pixel row: '+names_single[j], color=colors[j], marker='.' )
        
        if i//2==0:
            ax[i//2].set_ylabel('intensity [ADU]')
            
        if i//2==1:
            # ax[j].legend(fontsize=8, frameon=False, loc='upper left', bbox_to_anchor=(1.02,1))
            ax[i//2].legend(fontsize=8, frameon=False, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=3)
        # ax[0,0].set_xticks( np.arange(-1,1,5) )
        ax[i//2].set_xticks(wavelens_ranges[i//2])
        # ax[j].set_yticks(np.linspace(0, 4000,3))
        ax[i//2].tick_params(axis='both', labelsize=8 )
        ax[i//2].ticklabel_format(axis='y', style='sci', scilimits=(3,4) )
        
        
    ax[i//2].axvline(x=true_wavelens[i//2], color='black', linewidth=1, linestyle='--')


# # Hide the x-axis spines and ticks for both subplots
# ax[0,0].spines['bottom'].set_visible(False)
# ax[0,1].spines['bottom'].set_visible(False)
# ax[1,0].spines['top'].set_visible(False)
# ax[1,1].spines['top'].set_visible(False)

# Hide the y-axis spines and ticks for both subplots
ax[0].spines['right'].set_visible(False)
ax[1].spines['left'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[2].spines['left'].set_visible(False)
# ax[2].spines['right'].set_visible(False)
# ax[3].spines['left'].set_visible(False)
# ax[3].spines['right'].set_visible(False)


# # Hide the x-axis ticks and labels for the top plot
# ax[0].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
# ax[1].tick_params(axis='x', which='both', bottom=False, labelbottom=False)

# Hide the y-axis ticks and labels for the top plot
ax[1].tick_params(axis='y', which='both', left=False, labelleft=False)
ax[2].tick_params(axis='y', which='both', left=False, labelleft=False)
# ax[3].tick_params(axis='y', which='both', left=False, labelleft=False)

# # Draw a separation line between the two plots
# sep_line_y = 0 # Y-coordinate for the separation line
# ax[0].axhline(y=sep_line_y, color='black', linewidth=1, linestyle='--')
# ax[1].axhline(y=sep_line_y, color='black', linewidth=1, linestyle='--')

# Add slashes (`//`) on the separation line (top line of the bottom plot)
for i in range(2):
    slash_x_sep = ax[i].get_xlim()[1]  # X-coordinate where the slashes will be placed on the separation line
    slash_y_sep_down = ax[i].get_ylim()[0] 
    slash_y_sep_up = ax[i].get_ylim()[1] # Y-coordinate of the separation line
    ax[i].annotate('//', xy=(slash_x_sep, slash_y_sep_down), xytext=(slash_x_sep, slash_y_sep_down),
                 ha='center', va='center', fontsize=8, color='black',
                 bbox=dict(facecolor='white', edgecolor='none', pad=0))  # Add slashes with a white background
    ax[i].annotate('//', xy=(slash_x_sep, slash_y_sep_up), xytext=(slash_x_sep, slash_y_sep_up),
                 ha='center', va='center', fontsize=8, color='black',
                 bbox=dict(facecolor='white', edgecolor='none', pad=0))  # Add slashes with a white background


# # Ensure the x-axis ticks and labels are visible on the bottom plot
# ax[3].tick_params(axis='x', which='both', bottom=True, labelbottom=True)

# # Add a text box to the top plot
# ax[0].text(0.035, 0.87, 'PMMA', transform=ax[0].transAxes, fontsize=8, color='#ff42ffff',
#         )

# ax[3].text(0.035, -0.1, 'Polystyrene', transform=ax[0].transAxes, fontsize=8, color='#40f940ff',
#         )

# label the bottom x-axis
fig.text(0.51, 0.04, 'wavelength [nm]', ha='center', va='center', fontsize=10)
# fig.text( 0.03, 0.51, 'counts [a.u.]', ha='center', va='center', fontsize=10)
# fig.tight_layout()

# save figure
plot_path = os.path.join(plots_directory, 'plot_regions.png')
fig.savefig(plot_path, dpi=300)

# Display the plots
plt.show()

#%%
# CALCULATIONS

# wavelength center of mass

c_masses = {}
std = {}

for i in range(0,6,2):
    
    c_masses[ str(true_wavelens[i//2]) ] = []
    std[ str(true_wavelens[i//2]) ] = []
    
    for j in range(3):
        
        x = wavelens[i//2]
        y = summs[j][speclines_index[i]:speclines_index[i+1]]
        c_mass = np.sum( x * y ) / np.sum( y )
        c_masses[ str(true_wavelens[i//2]) ].append( round(c_mass, 3) )
        
        variance = np.sum( y * (x - c_mass)**2 ) / np.sum( y )
        sigma = np.sqrt( variance )
        std[ str(true_wavelens[i//2]) ].append( round(sigma, 3) )
        

