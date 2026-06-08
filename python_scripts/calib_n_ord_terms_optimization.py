#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:17:39 2024

@author: fernandoaguila
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import logging

from math_geom_model_functions import (
    math_geom_model,
    math_geom_model_cuad,
    math_geom_model_cubquint,
    math_geom_model_seventh,
    math_geom_model_seventh_centershift,
)
from center_mass_2 import center_mass

#%%

# Configure logging
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler('hyperspec_calibration.log')
console_handler = logging.StreamHandler()

file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants and configurations
PIXEL_SIZE_MM = 6.5e-3  # Pixel dimension in mm

# Define a dictionary for model functions mapping
MODEL_FUNCTIONS = {
    'zero_order': math_geom_model,
    'quadratic': math_geom_model_cuad,
    'cubic_quintic': math_geom_model_cubquint,
    'seven_order': math_geom_model_seventh,
    'seven_order_center_shift': math_geom_model_seventh_centershift,
}

# Default parameters for different orders
DEFAULT_PARAMS = {
    'zero_order': [90, 0.0, 0.0, -5.9, -25.9, 0.0, 0.0, 0.0, 0.0, 100, 0.0],
    'quadratic': [90, 0.0, 0.0, -5.9, -25.9, 0.0, 0.0, 0.0, 0.0, 100, 0.0, 0.0, 0.0],
    'cubic_quintic': [90, 0.0, 0.0, -5.9, -25.9, 0.0, 0.0, 0.0, 0.0, 100, 0.0, 0.0, 0.0, 0.0, 0.0],
    'seven_order': [90, 0.0, 0.0, -5.9, -25.9, 0.0, 0.0, 0.0, 0.0, 100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'seven_order_center_shift': [90, 0.0, 0.0, -5.9, -25.9, 0.0, 0.0, 0.0, 0.0, 100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
}

# Parameter names for different orders
PARAMETER_NAMES = {
    'zero_order': ['Phi', 'phi_d1', 'phi_d2', 'thetai', 'thetae', 'xi0', 'xo0', 'yi0', 'yo0', 'f1', 'rot'],
    'quadratic': ['Phi', 'phi_d1', 'phi_d2', 'thetai', 'thetae', 'xi0', 'xo0', 'yi0', 'yo0', 'f1', 'rot', 'a', 'b'],
    'cubic_quintic': ['Phi', 'phi_d1', 'phi_d2', 'thetai', 'thetae', 'xi0', 'xo0', 'yi0', 'yo0', 'f1', 'rot', 'a1', 'a2', 'b1', 'b2'],
    'seven_order': ['Phi', 'phi_d1', 'phi_d2', 'thetai', 'thetae', 'xi0', 'xo0', 'yi0', 'yo0', 'f1', 'rot', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6'],
    'seven_order_center_shift': ['Phi', 'phi_d1', 'phi_d2', 'thetai', 'thetae', 'xi0', 'xo0', 'yi0', 'yo0', 'f1', 'rot', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'Px0p', 'Py0p'],
}

# Parameters units
PARAMETER_UNITS = {
    'zero_order': ['deg', 'deg', 'deg', 'deg', 'deg', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg'],
    'quadratic': ['deg', 'deg', 'deg', 'deg', 'deg', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg', '1/mm', '1/mm^2'],
    'cubic_quintic': ['deg', 'deg', 'deg', 'deg', 'deg', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg', '1/mm', '1/mm^2', '1/mm^3', '1/mm^4'],
    'seven_order': ['deg', 'deg', 'deg', 'deg', 'deg', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg', '1/mm', '1/mm^2', '1/mm^3', '1/mm^4', '1/mm^5', '1/mm^6'],
    'seven_order_center_shift': ['deg', 'deg', 'deg', 'deg', 'deg', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg', '1/mm', '1/mm^2', '1/mm^3', '1/mm^4', '1/mm^5', '1/mm^6', 'mm', 'mm'],
}

#%%

def load_image(data_directory):
    """
    Load the center mass image from a .npy file.
    """
    file_path = os.path.join(data_directory, f'img_centermass.npy')
    try:
        img_centermass = np.load(file_path)
        logger.info(f"\nLoaded image data from {file_path}")
        return img_centermass
    except FileNotFoundError:
        logger.error(f"\nFile not found: {file_path}")
        raise


def load_neon_lines(data_directory, neon_file_name, selected_lines=None):
    """
    Load neon spectral lines from a text file and select specific lines if provided.
    """
    file_path = os.path.join(data_directory, neon_file_name)
    try:
        with open(file_path, 'r') as file:
            neon_lines = np.array([float(line.strip()) for line in file])
        logger.info(f"\nLoaded neon lines from {file_path}")
        if selected_lines is not None:
            neon_lines = neon_lines[selected_lines]
            logger.info(f"\nSelected specific neon lines: {neon_lines}")
        return neon_lines
    except FileNotFoundError:
        logger.error(f"\nFile not found: {file_path}")
        raise

#%%

def compute_center_mass(img_centermass, slit_length=12.9, slit_sep=0.3):
    """
    Compute the center of mass and anchor points for the slit mask.
    """
    n_holes = int(slit_length / slit_sep)
    anchor_points_pos = np.arange(n_holes)
    
    cmass_dic = center_mass(
        img_centermass,
        anchor_points_pos,
        length=slit_length,
        separation=slit_sep
    )
    
    x = cmass_dic['cmass_x']
    y = cmass_dic['cmass_y']
    x_m = np.array(cmass_dic['anchor_points_x'])
    y_m = np.array(cmass_dic['anchor_points_y'])
    cspec_lines = cmass_dic['chosen_spectral_lines']
    
    logger.info("\nComputed center mass and anchor points.")
    
    return {
        'x': x,
        'y': y,
        'x_m': x_m,
        'y_m': y_m,
        'cspec_lines': cspec_lines,
        'number_spectral_lines': len(cspec_lines),
        'anchor_points_pos': anchor_points_pos,
        'n_holes': n_holes,
        'num_anchor_points': len(anchor_points_pos)
    }

#%%

def simulate_spectral_lines(order, slit_sim, neon_lines, params):
    """
    Simulate spectral lines using the specified mathematical geometric model.
    """
    model_func = MODEL_FUNCTIONS.get(order)
    if not model_func:
        logger.error(f"\nUnknown order '{order}'. Available orders: {list(MODEL_FUNCTIONS.keys())}")
        raise ValueError(f"\nUnknown order '{order}'.")

    sim_x_list = []
    sim_y_list = []
    
    for wavelength in neon_lines:
        sim_y, sim_x = model_func(slit_sim, wavelength, *params)
        sim_x_list.append(sim_x)
        sim_y_list.append(sim_y)
    
    sim_x_array = np.array(sim_x_list)
    sim_y_array = np.array(sim_y_list)
    
    logger.info(f"\nSimulated spectral lines for order '{order}'.")
    
    return sim_x_array, sim_y_array

#%%

def optimize_parameters(
    order,
    initial_params,
    xi_s,
    wavelens,
    x_m,
    y_m,
    num_anchor_points,
    method='Powell',
    tol=1e-8
):
    """
    Optimize model parameters to minimize the distance between simulated and measured anchor points.
    """
    model_func = MODEL_FUNCTIONS.get(order)
    if not model_func:
        logger.error(f"\nUnknown order '{order}'. Available orders: {list(MODEL_FUNCTIONS.keys())}")
        raise ValueError(f"\nUnknown order '{order}'.")

    def objective_function(params):
        total_distance = 0
        for i, wavelength in enumerate(wavelens):
            sim_y, sim_x = model_func(xi_s, wavelength, *params)
            idx_start = i * num_anchor_points
            idx_end = idx_start + num_anchor_points
            dist_x = sim_x - x_m[idx_start:idx_end]
            dist_y = sim_y - y_m[idx_start:idx_end]
            distance = np.sqrt(dist_x**2 + dist_y**2).sum()
            total_distance += distance
        return total_distance

    result = opt.minimize(
        objective_function,
        initial_params,
        method=method,
        options={'ftol': tol, 'maxiter': 10000}
    )

    if result.success:
        logger.info(f"\nOptimization successful. Method: {method}, Iterations: {result.nit}")
    else:
        logger.warning(f"\nOptimization failed. Message: {result.message}")

    optimized_params = result.x
    final_distance = result.fun

    return optimized_params, final_distance, result

#%%

def plot_results(
    sim_x,
    sim_y,
    sim_x_opt,
    sim_y_opt,
    x,
    y,
    x_m,
    y_m,
    x_s_opt,
    y_s_opt,
    order,
    data_directory
):
    """
    Plot and compare the measured and simulated spectral lines before and after optimization.
    """
    fig, ax=plt.subplots(1,1, figsize=(10,8))
    ax.set_title(f'Optimization Results for {order}')
    
    # Plot measured data
    # ax.scatter(x, y, s=1.5, color='blue', alpha=0.5, label='Measured Data')
    ax.scatter(x_m, y_m, s=15, color='navy', alpha=0.7, label='Measured Anchor Points')
    
    # Plot simulated data before optimization
    # for i in range(sim_x.shape[0]):
    #     ax.scatter(sim_x[i], sim_y[i], s=1.5, color='red', alpha=0.3)
    # ax.scatter([], [], s=1.5, color='red', alpha=0.3, label='Simulated Data (Initial)')
    
    # Plot simulated data after optimization
    for i in range(sim_x_opt.shape[0]):
        ax.scatter(sim_x_opt[i], sim_y_opt[i], s=15, color='red', alpha=0.3)
    ax.scatter([], [], s=15, color='red', alpha=0.3, label='Simulated Data (Optimized)')
    
    # Plot optimized anchor points
    # ax.scatter(x_s_opt, y_s_opt, s=15, color='darkred', alpha=0.7, label='Optimized Anchor Points')
    
    # Draw arrows showing displacement
    ax.quiver(
        x_m,
        y_m,
        x_s_opt - x_m,
        y_s_opt - y_m,
        angles='xy',
        scale_units='xy',
        scale=0.01,
        color='orange',
        alpha=0.6,
        width=0.002,
        headwidth=3,
        headlength=5,
        label='Displacement Vectors'
    )
    
    ax.invert_yaxis()
    ax.set_xlabel('Pixel X')
    ax.set_ylabel('Pixel Y')
    ax.legend( ncol=1, markerscale=1.0, bbox_to_anchor=(1, 1))
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    
    # Save plot
    plot_path = os.path.join(data_directory, f'optimization_result_{order}.tif')
    fig.savefig(plot_path, dpi=400)
    # plt.close()
    logger.info(f"\nPlot saved to {plot_path}")
    
#%%

def hyperspec_calibration(
    working_directory,
    order,
    neon_file_name='neon_lines_calibration_02052024.txt',
    slit_length=12.9,
    slit_sep=0.3,
    optimization_method='Powell',
    optimization_tolerance=1e-8
):
    """
    Perform hyperspectral calibration using specified geometric model and optimization.
    """
    
    logger.info(f"\nStarting hyperspectral calibration for order '{order}'.")
    
    # DATA FOLDER
    data_directory = os.path.join(working_directory, 'calibration_data')

    # Load data
    img_centermass = load_image(data_directory)
    neon_lines = load_neon_lines(data_directory, neon_file_name)
    
    # Compute center mass and anchor points
    cmass_data = compute_center_mass(img_centermass, slit_length, slit_sep)
    x, y, x_m, y_m, cspec_lines, anchor_points_pos, n_holes, num_anchor_points = (
        cmass_data['x'],
        cmass_data['y'],
        cmass_data['x_m'],
        cmass_data['y_m'],
        cmass_data['cspec_lines'],
        cmass_data['anchor_points_pos'],
        cmass_data['n_holes'],
        cmass_data['num_anchor_points'],
    )
    
    # Save Numpy arrays for measured and anchor points 
    x_path = os.path.join(data_directory, 'x_measured.npy')
    np.save(x_path, x)
    y_path = os.path.join(data_directory, 'y_measured.npy')
    np.save(y_path, y)
    x_m_path = os.path.join(data_directory, 'x_anchor_measured.npy')
    np.save(x_m_path, x_m)
    y_m_path = os.path.join(data_directory, 'y_anchor_measured.npy')
    np.save(y_m_path, y_m)
    
    # Select wavelengths corresponding to chosen spectral lines
    wavelens = neon_lines[cspec_lines]
    
    # Generate slit simulation positions
    slit_sim = np.arange(-slit_length / 2, slit_length / 2, slit_sep)
    
    # Initial simulation
    initial_params = DEFAULT_PARAMS.get(order)
    if initial_params is None:
        logger.error(f"\nNo default parameters found for order '{order}'.")
        return
    
    sim_x_initial, sim_y_initial = simulate_spectral_lines(order, slit_sim, neon_lines, initial_params)
    
    # Save Numpy arrays for simulated measured anchor points
    sim_x_initial_path = os.path.join(data_directory, f'x_anchor_simulated_{order}.npy')
    np.save(sim_x_initial_path, sim_x_initial)
    sim_y_initial_path = os.path.join(data_directory, f'y_anchor_simulated_{order}.npy')
    np.save(sim_y_initial_path, sim_y_initial)
    
    
    # Prepare anchor points from initial simulation
    anchor_indices = (n_holes - 1) - anchor_points_pos
    x_s_initial = []
    y_s_initial = []
    for i in cspec_lines:
        for j in anchor_indices:
            x_s_initial.append(sim_x_initial[i][j])
            y_s_initial.append(sim_y_initial[i][j])
    x_s_initial = np.array(x_s_initial)
    y_s_initial = np.array(y_s_initial)
    
    # Save Numpy arrays for simulated ordered measured anchor points
    x_s_initial_path = os.path.join(data_directory, f'x_anchor_simulated_ordered_{order}.npy')
    np.save(x_s_initial_path, x_s_initial)
    y_s_initial_path = os.path.join(data_directory, f'y_anchor_simulated_ordered_{order}.npy')
    np.save(y_s_initial_path, y_s_initial)
    
    # Compute initial average distance
    initial_distances = np.sqrt((x_s_initial - x_m)**2 + (y_s_initial - y_m)**2)
    avg_initial_distance = np.mean(initial_distances)
    logger.info(f"\nInitial average distance: {avg_initial_distance:.4f} pixels ({avg_initial_distance * PIXEL_SIZE_MM:.4f} mm)")
    
    # Optimization
    xi_s = slit_sim[anchor_indices]
    optimized_params, final_distance, optimization_result = optimize_parameters(
        order,
        initial_params,
        xi_s,
        wavelens,
        x_m,
        y_m,
        num_anchor_points,
        method=optimization_method,
        tol=optimization_tolerance
    )
    
    # Simulate with optimized parameters
    sim_x_optimized, sim_y_optimized = simulate_spectral_lines(order, slit_sim, neon_lines, optimized_params)
    
    # Save Numpy arrays for optimized simulated measured anchor points
    sim_x_optimized_path = os.path.join(data_directory, f'x_anchor_opt_simulated_{order}.npy')
    np.save(sim_x_optimized_path, sim_x_optimized)
    sim_y_optimized_path = os.path.join(data_directory, f'y_anchor_opt_simulated_{order}.npy')
    np.save(sim_y_optimized_path, sim_y_optimized)
    
    # Prepare optimized anchor points
    x_s_optimized = []
    y_s_optimized = []
    for i in cspec_lines:
        for j in anchor_indices:
            x_s_optimized.append(sim_x_optimized[i][j])
            y_s_optimized.append(sim_y_optimized[i][j])
    x_s_optimized = np.array(x_s_optimized)
    y_s_optimized = np.array(y_s_optimized)
    
    # Save Numpy arrays for optimized ordered simulated measured anchor points
    x_s_optimized_path = os.path.join(data_directory, f'x_anchor_opt_ordered_simulated_{order}.npy')
    np.save(x_s_optimized_path, x_s_optimized)
    y_s_optimized_path = os.path.join(data_directory, f'y_anchor_opt_ordered_simulated_{order}.npy')
    np.save(y_s_optimized_path, y_s_optimized)    
    
    # Compute optimized average distance
    optimized_distances = np.sqrt((x_s_optimized - x_m)**2 + (y_s_optimized - y_m)**2)
    avg_optimized_distance = np.mean(optimized_distances)
    min_distance = np.min(optimized_distances)
    max_distance = np.max(optimized_distances)
    
    logger.info(f"\nOptimized average distance: {avg_optimized_distance:.4f} pixels ({avg_optimized_distance * PIXEL_SIZE_MM:.4f} mm)")
    logger.info(f"\nMinimum distance: {min_distance:.4f} pixels ({min_distance * PIXEL_SIZE_MM:.4f} mm)")
    logger.info(f"\nMaximum distance: {max_distance:.4f} pixels ({max_distance * PIXEL_SIZE_MM:.4f} mm)")
    
    # Save optimized parameters
    # numpy list
    params_numpy_path = os.path.join(data_directory, f'optimized_parameters_{order}_units.npy')
    np.save(params_numpy_path, optimized_params)
    ## txt file
    params_list= list(zip(PARAMETER_NAMES[order], optimized_params, PARAMETER_UNITS[order]))
    params_list.append(('f2', 100, 'mm'))  # Assuming fixed value
    params_list.append(('lines', 900, 'no units'))  # Assuming fixed value
    params_file_path = os.path.join(data_directory, f'optimized_parameters_{order}_units.txt')
    with open(params_file_path, 'w') as f:
        for param, value, unit in params_list:
            f.write(f"{param}\t{value}\t{unit}\n")
    logger.info(f"\nOptimized parameters saved to {params_file_path}")
    
    # Plot results
    plot_results(
        sim_x_initial,
        sim_y_initial,
        sim_x_optimized,
        sim_y_optimized,
        x,
        y,
        x_m,
        y_m,
        x_s_optimized,
        y_s_optimized,
        order,
        data_directory
    )
    
    logger.info("Hyperspectral calibration completed successfully.")