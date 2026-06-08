#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:26:30 2023

@author: fernandoaguila
"""

import numpy as np
from math_geom_model_functions import (
    math_geom_model,
    math_geom_model_cuad,
    math_geom_model_cubquint,
    math_geom_model_seventh,
    math_geom_model_seventh_centershift,
)
from scipy.interpolate import RegularGridInterpolator
import scipy.io
import os
import logging

MODEL_FUNCTIONS = {
    'zero_order': math_geom_model,
    'quadratic': math_geom_model_cuad,
    'cubic_quintic': math_geom_model_cubquint,
    'seven_order': math_geom_model_seventh,
    'seven_order_center_shift': math_geom_model_seventh_centershift,
}

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

def grid_generator(mask, slit_dim, wavelen_range, parameters, data_directory, order='seven_order'):
    
    insize = mask.shape[0]
    
    ## number of points for the slit dimension simulation 
    outsizeX = insize
    
    ## top and bottom coordinates of the slit(note that the center of the slit has value 0)
    outcominX, outcommaxX = slit_dim
    
    ## number of points for the wavelength range
    outsizeL = insize
    outcominL, outcommaxL = wavelen_range
    
    ## Creating a coordinate system (grid) where we are interested in their interpolated values. That is create a grid where the values are gonna be
    ## interpolated from
    
    xi, lamda = np.meshgrid(np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True), 
                            np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True), indexing='ij')
    
    xi_saving = np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True)
    lamda_saving = np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True)
    # print(xi)
    
    ## Saving position and wavelength arrays
    xi_data_path = os.path.join(data_directory, 'xi')
    lamda_data_path = os.path.join(data_directory, 'wavelengths')
    np.save(xi_data_path, xi_saving)
    np.save(lamda_data_path, lamda_saving)
    
    ## Calculating simulated values in the whole grid
    model_func = MODEL_FUNCTIONS.get(order)
    
    if not model_func:
        logger.error(f"\nUnknown order '{order}'. Available orders: {list(MODEL_FUNCTIONS.keys())}")
        raise ValueError(f"\nUnknown order '{order}'.")
        
    xo, yo = model_func( xi, lamda, *parameters)
    
    ## testpoints on the rawdata
    test_points = np.array([xo.ravel(), yo.ravel()]).T   
    # print(f"test_points shape: {np.shape(test_points)}")
     
    # print('\nmiminum of x0:',np.min(xo))
    # print('maximum of x0:',np.max(xo))
    
    # print('\nmiminum of y0:',np.min(yo))
    # print('maximum of y0:',np.max(yo))
    
    ##  number of points according to the number of pixels in the image
    insize=mask.shape[0] #2048
    incomin = 0 # position of the origin of the original image, i.e., index of the first column/row
    

    ## Suppose we only know some data on a regular grid.
    ## creating the points defining the coordinate system (grid) with length same as extended image dimension (destination grid)
    fit_points = [np.linspace(incomin, insize, insize, endpoint=True), np.linspace(incomin, insize, insize, endpoint=True)]      # data grid                  
       
    return [test_points, fit_points]

def grid_generator_padding(mask, slit_dim, wavelen_range, parameters, data_directory, order='seven_order'):
    
    insize = mask.shape[0]
    
    ## number of points for the slit dimension simulation   
    outsizeX = insize+20
    
    ## top and bottom coordinates of the slit(note that the center of the slit has value 0)
    outcominX, outcommaxX = slit_dim
    
    ## number of points for the wavelength range
    outsizeL=outsizeX
    outcominL, outcommaxL = wavelen_range
    
    ## Creating a coordinate system (grid) where we are interested in their interpolated values. That is create a grid where the values are gonna be
    ## interpolated from
    xi, lamda = np.meshgrid(np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True), 
                            np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True), indexing='ij')
    
    xi_saving = np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True)
    lamda_saving = np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True)
    # print(xi)
    
    ## Saving position and wavelength arrays
    xi_data_path = os.path.join(data_directory, 'xi_padding')
    lamda_data_path = os.path.join(data_directory, 'wavelengths_padding')
    np.save(xi_data_path, xi_saving)
    np.save(lamda_data_path, lamda_saving)
    
    ## Calculating simulated values in the whole grid
    model_func = MODEL_FUNCTIONS.get(order)
    
    if not model_func:
        logger.error(f"\nUnknown order '{order}'. Available orders: {list(MODEL_FUNCTIONS.keys())}")
        raise ValueError(f"\nUnknown order '{order}'.")
 
    xo, yo = model_func( xi, lamda, *parameters)
    
    ## testpoints on the rawdata
    test_points = np.array([xo.ravel(), yo.ravel()]).T   
    # print(f"test_points shape: {np.shape(test_points)}")
    
    # print('\nmiminum of x0:',np.min(xo))
    # print('maximum of x0:',np.max(xo))
    
    # print('\nmiminum of y0:',np.min(yo))
    # print('maximum of y0:',np.max(yo))
    
    ##  number of points according to the number of pixels in the image
    insize=mask.shape[0] #2048
    incomin = 0 # position of the origin of the original image, i.e., index of the first column/row
    

    ## Suppose we only know some data on a regular grid.
    ## creating the points defining the coordinate system (grid) with length same as extended image dimension (destination grid)
    fit_points = [np.linspace(incomin, insize, insize, endpoint=True), np.linspace(incomin, insize, insize, endpoint=True)]      # data grid                  
       
    return [test_points, fit_points]

def grid_generator_manyimages(mask, number_images, slit_dim, wavelen_range, parameters, file_name, data_directory, order='seven_order'):
    
    insize = mask.shape[0]
    
    ## number of points for the slit dimension simulation 
    outsizeX = insize
    
    ## top and bottom coordinates of the slit(note that the center of the slit has value 0)
    outcominX, outcommaxX = slit_dim
    
    ## number of points for the wavelength range
    outsizeL = insize
    outcominL, outcommaxL = wavelen_range
    
    ## Creating a coordinate system (grid) where we are interested in their interpolated values. That is create a grid where the values are gonna be
    ## interpolated from
    xi, lamda, image_number = np.meshgrid(np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True), 
                                          np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True), 
                                          np.linspace(1, number_images, number_images, endpoint=True), indexing='ij')
    
    xi_saving = np.linspace(outcommaxX,outcominX, outsizeX, endpoint=True)
    lamda_saving = np.linspace(outcominL, outcommaxL, outsizeL, endpoint=True)
    # print(xi)
    
    ## Saving position and wavelength arrays
    xi_data_path = os.path.join(data_directory, 'xi_many')
    lamda_data_path = os.path.join(data_directory, 'wavelengths_many')
    np.save(xi_data_path, xi_saving)
    np.save(lamda_data_path, lamda_saving)
    
    ## Calculating simulated values in the whole grid
    model_func = MODEL_FUNCTIONS.get(order)
    
    if not model_func:
        logger.error(f"\nUnknown order '{order}'. Available orders: {list(MODEL_FUNCTIONS.keys())}")
        raise ValueError(f"\nUnknown order '{order}'.")
        
    xo, yo = model_func( xi, lamda, *parameters)
    
    ## testpoints on the rawdata
    test_points = np.array([xo.ravel(), yo.ravel(), image_number.ravel()]).T  
    
    insize=mask.shape[0] #2048
    incomin = 0 # position of the origin of the original image, i.e., index of the first column/row
    

    ## Suppose we only know some data on a regular grid.
    ## creating the points defining the coordinate system (grid) with length same as extended image dimension (destination grid)
    fit_points = [np.linspace(incomin, insize, insize, endpoint=True), 
                  np.linspace(incomin, insize, insize, endpoint=True), 
                  np.linspace(1, number_images, number_images, endpoint=True)]      # data grid                  
       
    return [test_points, fit_points]
    
def interpolator(mask, fit_points, test_points, method='linear'):
    """
    Function that calculates the interpolation of the mask according to the specified method

    Parameters
    ----------
    mask : Array of bool
        mask of the corrected measured inage.
    fit_points : ndarray
        x mathematical geometrical model values grid.
    yo : ndarray
        y mathematical geometrical model values grid.
    method : String, optional
        method used for the interpolation. The default is 'linear'.

    Returns
    -------
    result: Array of float64 shape(n*m)
        a: Interpolated image according to the given method.

    """
    
    ## We can define interpolator function from the points that define the grid and the measured data 
    insize=mask.shape
    
    interp = RegularGridInterpolator(fit_points, mask, bounds_error=False, fill_value=0)
    # result=interp(test_points, method).reshape(insize)
    result=interp(test_points, method)
    
    
    return result
    
    
    
    