#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 14:46:41 2024

@author: fernandoaguila
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io
import logging 
from natsort import natsorted
import tifffile as tf

# Configure logging
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler('hyperspec_calibration_optimization_visual_gpt_f.log')
console_handler = logging.StreamHandler()

file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Function to find the maximums in an image within a specified column range [a, b]
def locmax(img, a, b):  
    try:
        return np.argmax(img[:, a:b], axis=1)
    except Exception as e:
        print(f"Error in locmax: {e}")
        return None

# Function to apply gamma correction to an image
def gamma(img, gamma_val):
    try:
        return img ** (1 / gamma_val)
    except Exception as e:
        print(f"Error in gamma function: {e}")
        return None

# Function to adjust image contrast and gamma
def contrast_gamma(img_in, min_in, max_in, min_out, max_out, gamma):
    try:
        img_clipped = np.clip((img_in.astype(np.float32) - min_in) / (max_in - min_in), 0, 1)
        return (img_clipped ** gamma) * (max_out - min_out) + min_out
    except Exception as e:
        print(f"Error in contrast_gamma: {e}")
        return None
    
# Function to convert matlab files to python files
def matlab_to_python(results_directory, folder_name, file_ext='.mat'):
    interpolation_images_path = os.path.join(results_directory, folder_name+'_matlab_results')

    # Change to the results directory and load image filenames
    logger.info(f"Accessing directory: {interpolation_images_path}")
    image_content = []
    with os.scandir(interpolation_images_path) as entries:
        sorted_entries = natsorted(entries, key=lambda entry:entry.name)
        # print(sorted_entries)
        for entry in sorted_entries:
            if entry.is_file() and entry.name.endswith(file_ext):
                image = scipy.io.loadmat(entry)
                image_content.append(image['interpolation'])
            
    
    if not image_content:
        logger.error(f"No files matching '{file_ext}' found in directory '{interpolation_images_path}'.")
        raise FileNotFoundError(f"No files matching '{file_ext}' found in directory '{interpolation_images_path}'.")
        
    # Creating the folders to save the convertion result
    python_folder = os.path.join(interpolation_images_path, 'python')
    
    if not os.path.exists(python_folder):
        os.mkdir(python_folder)
        logger.info(f'New directory created: {python_folder}')
    else:
        logger.info(f'Folder {python_folder} already exists')
    
    # Number of images
    l = len(image_content)
    logger.info(f"Found {l} images matching the file extension '{file_ext}'")
    
    # Saving numpy arrays
    
    for i in range(l):
        python_converted_path = os.path.join(python_folder, f'interpolated_image_{i}')
        np.save(python_converted_path, image_content[i])
        
    logger.info("Conversion and storage completed")

# Main function to visualize the optimization process
def opt_visual( data_directory,  order):
    try:
        # Loading necessary arrays
        x = np.load(os.path.join(data_directory, 'x_measured.npy'))
        y = np.load(os.path.join(data_directory, 'y_measured.npy'))

        x_m = np.load(os.path.join(data_directory, 'x_anchor_measured.npy'))
        y_m = np.load(os.path.join(data_directory, 'y_anchor_measured.npy'))

        x_s = np.load(os.path.join(data_directory, f'x_anchor_simulated_ordered_{order}.npy'))
        y_s = np.load(os.path.join(data_directory, f'y_anchor_simulated_ordered_{order}.npy'))

        sim_x = np.load(os.path.join(data_directory, f'x_anchor_simulated_{order}.npy'))
        sim_y = np.load(os.path.join(data_directory, f'y_anchor_simulated_{order}.npy'))

        sim_x_op = np.load(os.path.join(data_directory, f'x_anchor_opt_simulated_{order}.npy'))
        sim_y_op = np.load(os.path.join(data_directory, f'y_anchor_opt_simulated_{order}.npy'))

        x_s_p = np.load(os.path.join(data_directory, f'x_anchor_opt_ordered_simulated_{order}.npy'))
        y_s_p = np.load(os.path.join(data_directory, f'y_anchor_opt_ordered_simulated_{order}.npy'))

        img_centermass = np.load(os.path.join(data_directory, 'img_centermass.npy'))
        # mask_dialated = np.load(os.path.join(data_directory, 'mask_expand.npy'))
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    try:
        # Visualization
        size = 1.1
        size2 = 2
        alph = 0.5
        
    #     fig, ax = plt.subplots(1, 2, figsize=(8, 4))
        

    #     # Plotting the simulated spectral lines
    #     for i in range(len(sim_x)):
    #         ax[0].scatter(sim_x[i], sim_y[i], color='red', s=size, alpha=alph)
    #     ax[0].scatter(sim_x[0], sim_y[0], color='red', label='MGM', s=size, alpha=alph)

    #     # Plotting the measured spectral lines
    #     ax[0].scatter(x, y, s=size, color='blue', label='Measurement', alpha=alph)

    #     # Plotting mask
    #     ax[0].imshow(contrast_gamma(img_centermass, 0, 65535, 0, 255, 1/2.2), cmap='gray_r')

    #     # Plotting selected points
    #     ax[0].scatter(x_m, y_m, c='b', s=size2)
    #     ax[0].scatter(x_s, y_s, c='r', s=size2)

    #     # Arrows indicating separation distance and direction
    #     ax[0].plot([x_m, x_s], [y_m, y_s], ls='--', color='y', alpha=0.4)
    #     ax[0].quiver(x_m, y_m, x_s - x_m, y_s - y_m, angles='xy', scale_units='xy', scale=1, color='y', alpha=0.8)

    #     ax[0].set_xlabel('Pixel number')
    #     ax[0].set_ylabel('Pixel number')
    #     ax[0].legend(bbox_to_anchor=(1.07, 1), loc='upper left', fontsize='small', markerscale=2.0)

    #     # Average separation distance before optimization
    #     dist_x = x_s - x_m
    #     dist_y = y_s - y_m
    #     avg_dist = np.mean(np.sqrt(dist_x ** 2 + dist_y ** 2))
    #     print(f'\nAverage separation distance before optimization: {avg_dist} pixels or {avg_dist * 6.5e-3} mm\n')

    #     # Plotting of optimized spectrum and measured one
    #     for i in range(1, len(sim_x)):
    #         ax[1].scatter(sim_x_op[i], sim_y_op[i], color='red', s=size, alpha=alph)
    #     ax[1].scatter(sim_x_op[0], sim_y_op[0], color='red', label='Model', s=size, alpha=alph)

    #     ax[1].scatter(x, y, s=size, color='blue', label='Measurement', alpha=alph)
    #     ax[1].scatter(x_m, y_m, c='b', s=size2)
    #     ax[1].scatter(x_s_p, y_s_p, c='r', s=size2)

    #     ax[1].quiver(x_m, y_m, x_s_p - x_m, y_s_p - y_m, angles='xy', scale_units='xy', scale=0.01, color='y', alpha=0.8)

    #     ax[1].invert_yaxis()
    #     ax[1].imshow(contrast_gamma(img_centermass, 0, 65535, 0, 255, 1/2.2), cmap='gray_r')

    #     ax[1].set_xlabel('Pixel number')
    #     ax[1].set_ylabel('Pixel number')
    #     ax[1].yaxis.set_tick_params(which='both', right=True, left=False, labelleft=False, labelright=True)
    #     ax[1].yaxis.set_label_position('right')
    #     ax[1].set_xlim(0, 2048)

    #     fig.tight_layout()

    #     # Average separation distance after optimization
    #     distop_x = x_s_p - x_m
    #     distop_y = y_s_p - y_m
    #     distop = np.sqrt(distop_x ** 2 + distop_y ** 2)
    #     avgop_dist = np.mean(distop)
    #     min_dist_comparison = np.min(distop)
    #     max_dist_comparison = np.max(distop)

    #     print('\nSeventh order:')
    #     print(f'\nAverage separation distance after optimization: {avgop_dist} pixels or {avgop_dist * 6.5e-3} mm\n')
    #     print(f'\nMinimum distance after optimization: {min_dist_comparison} pixels or {min_dist_comparison * 6.5e-3} mm\n')
    #     print(f'\nMaximum distance after optimization: {max_dist_comparison} pixels or {max_dist_comparison * 6.5e-3} mm\n')
        
    #     # Saving the figure
    #     try:
    #         fig_path = os.path.join(data_directory, f'optimization_twospec_comparison_{order}.tif')
    #         fig.savefig(fig_path, dpi=400)
    #     except Exception as e:
    #         print(f"Error saving figure: {e}")

        
        # SEPARATE PLOTS
        
        # PLOTTING OF CALCULATED AND MEASURED SPECTRUM
        
        fig, ax = plt.subplots(1, 1,)
        
        # Plotting the measured spectral lines
        ax.scatter(x, y, s=size, color='blue', label='Measurement', alpha=alph)
        
        # Plotting the simulated spectral lines
        for i in range(len(sim_x)):
            ax.scatter(sim_x[i], sim_y[i], color='red', s=size, alpha=alph)
        ax.scatter(sim_x[0], sim_y[0], color='red', label='MGM', s=size, alpha=alph)

        # Plotting mask
        ax.imshow(contrast_gamma(img_centermass, 0, 65535, 0, 255, 1/2.2), cmap='gray_r')

        # Plotting selected points
        ax.scatter(x_m, y_m, c='b', s=size2)
        ax.scatter(x_s, y_s, c='r', s=size2)

        # Arrows indicating separation distance and direction
        ax.plot([x_m, x_s], [y_m, y_s], ls='--', color='y', alpha=0.2)
        ax.quiver(x_m, y_m, x_s - x_m, y_s - y_m, angles='xy', scale_units='xy', scale=1, color='y', alpha=0.2)

        ax.set_xlabel('Pixel number')
        ax.set_ylabel('Pixel number')
        ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize='small', markerscale=2.0)
        
        fig.tight_layout()
        
        # Saving the figure
        try:
            fig_path = os.path.join(data_directory, f'comparison_{order}.tif')
            fig.savefig(fig_path, dpi=400)
        except Exception as e:
            print(f"Error saving figure: {e}")

        # Average separation distance before optimization
        dist_x = x_s - x_m
        dist_y = y_s - y_m
        avg_dist = np.mean(np.sqrt(dist_x ** 2 + dist_y ** 2))
        print(f'\nAverage separation distance before optimization: {avg_dist} pixels or {avg_dist * 6.5e-3} mm\n')    
        
        # PLOTTING OF OPTIMIZED AND MEASURED SPECTRUM
        
        fig2, ax2 = plt.subplots(1, 1,)
        
        # Plotting the measured spectral lines
        ax2.scatter(x, y, s=size, color='blue', label='Measurement', alpha=alph)
        
        # Plotting the optimized simulated spectral lines
        for i in range(1, len(sim_x)):
            ax2.scatter(sim_x_op[i], sim_y_op[i], color='red', s=size, alpha=alph)
        ax2.scatter(sim_x_op[0], sim_y_op[0], color='red', label='Model', s=size, alpha=alph)
        
        # Plotting selected points
        ax2.scatter(x_m, y_m, c='b', s=size2)
        ax2.scatter(x_s_p, y_s_p, c='r', s=size2)

        ax2.quiver(x_m, y_m, x_s_p - x_m, y_s_p - y_m, angles='xy', scale_units='xy', scale=0.01, color='y', alpha=0.8)

        ax2.invert_yaxis()
        ax2.imshow(contrast_gamma(img_centermass, 0, 65535, 0, 255, 1/2.2), cmap='gray_r')

        ax2.set_xlabel('Pixel number')
        ax2.set_ylabel('Pixel number')
        ax2.yaxis.set_tick_params(which='both', right=False, left=True, labelleft=True, labelright=False)
        ax2.yaxis.set_label_position('left')
        ax2.set_xlim(0, 2048)

        fig2.tight_layout()
        
        # Saving the figure
        try:
            fig_path = os.path.join(data_directory, f'optimization_comparison_{order}.tif')
            fig2.savefig(fig_path, dpi=400)
        except Exception as e:
            print(f"Error saving figure: {e}")

        # Average separation distance after optimization
        distop_x = x_s_p - x_m
        distop_y = y_s_p - y_m
        distop = np.sqrt(distop_x ** 2 + distop_y ** 2)
        avgop_dist = np.mean(distop)
        min_dist_comparison = np.min(distop)
        max_dist_comparison = np.max(distop)

        print('\nSeventh order:')
        print(f'\nAverage separation distance after optimization: {avgop_dist} pixels or {avgop_dist * 6.5e-3} mm\n')
        print(f'\nMinimum distance after optimization: {min_dist_comparison} pixels or {min_dist_comparison * 6.5e-3} mm\n')
        print(f'\nMaximum distance after optimization: {max_dist_comparison} pixels or {max_dist_comparison * 6.5e-3} mm\n')

    except Exception as e:
            print(f"Error in visualization: {e}")
        
def interpolation_python_visual(results_directory, image_number, order, file_ext='.npy', slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668], min_val=0, max_val=10000):
    
    interpolation_results_directory = os.path.join(results_directory, f'{order}_interpolation_python')

    # # Change to the results directory and load image filenames
    # logger.info(f"Accessing directory: {interpolation_images_path}")
    # with os.scandir(interpolation_images_path) as entries:
    #     image_content = [np.load(entry.path) for entry in entries if entry.is_file() and entry.name.endswith(file_ext)]
        
    # Load interpolated python image
    python_int_name = os.path.join(interpolation_results_directory, f'image_{image_number:0{4}d}.npy')
    image_int_python = np.load(python_int_name)
    
    if not python_int_name:
        logger.error(f"No files matching '{python_int_name}' found.")
        raise FileNotFoundError(f"No files matching '{python_int_name}' found.")
        
    wavelen_range = np.array(wavelen_range)
    wavelen_range = 1e7/532 - (1e7/wavelen_range)
    
    # SAVING IMAGE
    plot_directory = os.path.join(interpolation_results_directory, 'plots')
    os.makedirs(plot_directory, exist_ok=True)
    image_path = os.path.join(plot_directory, f'cubicinterp_image_{image_number:0{4}d}.png')

    try:
        fig, axes = plt.subplots(1, 1)
        axes.imshow(image_int_python, extent=[wavelen_range[0], wavelen_range[1], slit_dim_range[0], slit_dim_range[1]], 
                    aspect='auto', cmap='gray_r',  vmin=min_val, vmax=max_val)
        # axes.imshow(image_int_python, aspect='auto', cmap='gray', vmin=min_val, vmax=max_val)
        # axes.set_yticks(np.arange(-6, 8, 2))
        axes.set_xlabel('Wavelength [1/cm]')
        axes.set_ylabel('Slit position [mm]')
        axes.grid(True, axis='x', color='blue')
        plt.show()
        fig.savefig(image_path, dpi=300)
        logger.info(f"Successfully plotted image {image_number+1}")
    except Exception as e:
        logger.error(f"Error during plotting for image '{image_number}': {e}")
        raise RuntimeError(f"Error during plotting for image '{image_number}': {e}")        
                
def interpolation_matlab_visual(results_directory, folder_name, image_number, file_ext='.npy', slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668], min_val=0, max_val=10000):
    
    interpolation_images_path = os.path.join(results_directory, folder_name+'_matlab_results')
    
    # interpolation_python_images_path = os.path.join(interpolation_images_path, 'python')

    # Change to the results directory and load image filenames
    # logger.info(f"Accessing directory: {interpolation_python_images_path}")
    # with os.scandir(interpolation_python_images_path) as entries:
    #     sorted_entries = natsorted(entries, key=lambda entry:entry.name)
    #     image_content = [np.load(entry.path) for entry in sorted_entries if entry.is_file() and entry.name.endswith(file_ext) ]
        
    # Loading matlab interpolation
    matlab_int_name = os.path.join(interpolation_images_path, f'interpolated_image_{image_number}.mat')
    image_int_matlab = scipy.io.loadmat(matlab_int_name)
    
    if not matlab_int_name:
        logger.error(f"No files matching '{matlab_int_name}' found.")
        raise FileNotFoundError(f"No files matching '{matlab_int_name}' found.")
    

    try:
        fig, axes = plt.subplots(1, 1)
        # axes.imshow(image_int_matlab, extent=[wavelen_range[0], wavelen_range[1], slit_dim_range[0], slit_dim_range[1]], 
        #             aspect='auto', cmap='gray', vmin=min_val, vmax=max_val)
        axes.imshow(image_int_matlab['interpolation'], aspect='auto', cmap='gray', vmin=min_val, vmax=max_val)
        # axes.set_yticks(np.arange(-6, 8, 2))
        # axes.set_xlabel('Wavelength [nm]')
        # axes.set_ylabel('Slit position [mm]')
        plt.show()
        logger.info(f"Successfully plotted image {image_number+1}")
    except Exception as e:
        logger.error(f"Error during plotting for image '{image_number}': {e}")
        raise RuntimeError(f"Error during plotting for image '{image_number}': {e}")   

def matlab_visual(matlab_directory, data_directory, file_name, order, umethod, slit_dim_range=[-6.45, 6.45], wavelen_range=[540, 668]):
    
    logger.info('Starting matlab_visual function')
    # load matlab interpolation
    
    logger.info(f'Loading matlab interpolation from {matlab_directory}')
    try:
        interpolation_matlab_path = os.path.join(matlab_directory, 'mask_'+file_name+'_interpolated_'+umethod)
        interpolation_matlab_dic = scipy.io.loadmat(interpolation_matlab_path)
        interpolation_matlab_image = np.float32(interpolation_matlab_dic['interpolation'])
    except Exception as e:
        logger.error(f'Error during loading of matlab interpolation: {e}')
        raise FileNotFoundError(f'No file {interpolation_matlab_path} found')
    
    # load python interpolation
    
    logger.info(f'Loading python interpolation from {data_directory}')
    
    try:
        interpolation_python_path = os.path.join(data_directory, f'image_interpolated_{order}_{file_name}.npy')
        interpolation_python_image = np.load(interpolation_python_path)
    except Exception as e:
        logger.error(f'Error during loading of python interpolation: {e}')
        raise FileNotFoundError(f'No file {interpolation_python_path} found')
    # substraction of both interpoltions
    
    logger.info('Substracting interpolations')
    substraction_interpolations = np.abs(interpolation_matlab_image-interpolation_python_image)
    if np.isnan(substraction_interpolations).any():
        print("The array contains NaN values.")
    else:
        max_substraction_interpolations = substraction_interpolations.max()
        # print(max_value)
    
    # Finding maximums
    max_matlab_interpolation = interpolation_matlab_image.max()
    max_python_interpolation = interpolation_python_image.max()
    
    
    # Calculating percentage of maximum of the substraction with respect to each interpolations
    percentage_matlab = (max_substraction_interpolations/max_matlab_interpolation)*100
    logger.info(f'The max of the substraction represents {percentage_matlab} of the matlab {umethod} interpolation') 
    percentage_python = (max_substraction_interpolations/ max_python_interpolation)*100
    logger.info(f'The max of the substraction represents {percentage_python} of the python {umethod} interpolation') 
    
    logger.info('Plotting results')
    # Plotting the result
    try:
        # plot of the hyperspectral image matlab
        fig, axes = plt.subplots(1, 1)
        axes.set_title(f'Matlab hyperspectral image of {file_name}')
        axes.imshow(interpolation_matlab_image, extent=[wavelen_range[0], wavelen_range[1], slit_dim_range[0], slit_dim_range[1]], 
                    aspect='auto', cmap='gray_r', vmin=0, vmax=1000)
        axes.set_yticks(np.arange(-6, 8, 2))
        axes.set_xlabel('Wavelength [nm]')
        axes.set_ylabel('Slit position [mm]')
        plt.show()
        
         # plot of the interpolated image matlab
        fig, axes = plt.subplots(1, 1)
        axes.set_title(f'Matlab {umethod} interpolation {file_name}')
        axes.imshow(interpolation_matlab_image, 
                    aspect='auto', cmap='gray_r', vmin=0, vmax=1000)
        
        axes.set_xlabel('pixel number')
        axes.set_ylabel('pixel number')
        plt.show()
        
        # plot interpolation image python 
        fig, axes = plt.subplots(1, 1)
        axes.set_title(f'Python {umethod} interpolation {file_name}')
        axes.imshow(interpolation_python_image, 
                    aspect='auto', cmap='gray_r', vmin=0, vmax=1000)
        
        axes.set_xlabel('pixel number')
        axes.set_ylabel('pixel number')
        plt.show()
        
        # plot interpolation substraction
        fig, axes = plt.subplots(1, 1)
        axes.set_title(f'substraction {umethod} interpolation {file_name}')
        axes.imshow(substraction_interpolations, 
                    aspect='auto', cmap='gray_r', vmin=0, vmax=100)
        axes.set_xlabel('pixel number')
        axes.set_ylabel('pixel number')
        plt.show()
        

    
        logger.info(f"Successfully plotted image: {interpolation_matlab_path}")
    except Exception as e:
        logger.error(f"Error during plotting for image '{interpolation_matlab_path}': {e}")
        raise RuntimeError(f"Error during plotting for image '{interpolation_matlab_path}': {e}")
        
def spectrum_visual(results_directory, data_directory,
                     umethod, image_number, row_u, row_l, 
                    ):
    
    images_directory = os.path.join(results_directory, f'{umethod}_interpolation_python')

    logger.info(f"Accessing directory: {images_directory}")
    
    # Loading specific image
    image_name = os.path.join(images_directory, f'image_{image_number:0{4}d}.npy')
    image = np.load(image_name)
    
    logger.info(f"Succesfully loaded: image_{image_number:0{4}d}.npy")
    
    if not image_name:
        logger.error(f"No file matching {image_name} found.")
        raise FileNotFoundError(f"No file matching {image_name} found.")
        
    # Load position and wavelength arrays 
    logger.info(f"Accessing directory: {data_directory}")
    xi_path_name = os.path.join(data_directory, 'xi.npy')
    wavelen_path_name = os.path.join(data_directory, 'wavelengths.npy')
    xi = np.load(xi_path_name)
    wavelen = np.load(wavelen_path_name)
    # raman shift 
    wavelen_shift = 1e7/532 - (1e7/wavelen)
    
    
    ## Average
    average_spectra_center = np.average(image[row_u:row_l, ::], axis=0)

    
    # save python array
    plot_directory = os.path.join(results_directory, 'plots')
    os.makedirs(plot_directory, exist_ok=True)
    array_path = os.path.join(plot_directory, f'plot_spectral_image_{image_number:0{4}d}_{row_u}_to_{row_l}')
    np.save(array_path, average_spectra_center)
    
    folder_plot_path = os.path.join(results_directory, 'plots')
    plot_path = os.path.join(folder_plot_path, f'plot_spectral_image_{image_number:0{4}d}_{row_u}_to_{row_l}')

    try:
        # PLOT OF WAVELENGTHS [NM]
        # fig, axes = plt.subplots(1, 1)
        # axes.set_title(f'Average of image {image_number:0{4}d}, row sections: {row_u} to {row_l} for ')
        # axes.plot(wavelen, average_spectra_center)
        # # axes.plot(average_spectra)
        # axes.set_xlabel('Wavelength [nm]')
        # axes.set_ylabel('Intensity')
        # plt.show()
        
        # PLOT OF WAVE-NUMBERS [1/CM]
        fig, axes = plt.subplots(1, 1)
        axes.set_title(f'Average of image {image_number:0{4}d}, row sections: {row_u} to {row_l}')
        # axes.plot(wavelen_shift, average_spectra_up)
        axes.plot(wavelen_shift, average_spectra_center)
        # axes.plot(wavelen_shift, average_spectra_down)
        axes.set_xlabel('Raman shift [1/cm]')
        axes.set_ylabel('Counts [a.u.]')
        fig.savefig(plot_path, dpi=300)
        plt.show()
        
        logger.info(f"Successfully plotted from image_{image_number:0{4}d} average of row sections: {row_u} to {row_l}, or positons: {xi[row_u]} mm to {xi[row_l]} mm")
    except Exception as e:
        logger.error(f"Error during plotting for average row sections {row_u} to {row_l}: {e}")
        raise RuntimeError(f"Error during plotting for average row sections {row_u} to {row_l}: {e}")      
        
def spectrum_roi(results_directory, data_directory, folder_name, folder_plot_save,
                    test, image_number, col_1, file_ext='.npy'):
    images_directory = os.path.join(results_directory, folder_name)

    # logger.info(f"Accessing directory: {images_directory}")
    
    # Loading specific image
    image_name = os.path.join(images_directory, 'image_'+image_number+'.npy')
    image = np.load(image_name)
    
    # logger.info("Succesfully loaded: image_"+image_number+".npy")
    
    if not image_name:
        logger.error(f"No file matching {image_name} found.")
        raise FileNotFoundError(f"No file matching {image_name} found.")
        
    
    ## Average
    # average_spectra = np.average(image[col_1:col_2+1, ::], axis=0)
    # average_spectra_up = np.average(image[5:6, ::], axis=0)
    return image[col_1, ::]
    
    
