# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:13:38 2026

@author: aguilafernando
"""

import numpy as np
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

project_directory = os.path.dirname(script_directory)
data_directory = os.path.join(project_directory, "data")

date = '20260505'

sample = 'PS3_3'

ROI = '01'

test = '01'

folder_name =  date+'_'+sample+'_ROI'+ROI+'_test'+test
working_directory = os.path.join(project_directory, folder_name)


DataPfad = os.path.join(working_directory, 'raw')

RaTiffliste = [f for f in os.listdir(DataPfad) if f.endswith(".txt") ]
filename = DataPfad +"/"+ RaTiffliste[0] 
numtiffimg = len(RaTiffliste)

def read_data_from_txt(filename):
    """
    Read floating point numbers from a tab-separated text file.
    
    Parameters:
    filename (str): Path to the input text file
    
    Returns:
    tuple: (x_values, data_matrix) where:
        - x_values: 1D numpy array of shape (n,) containing first column values
        - data_matrix: 2D numpy array of shape (n, m-1) containing remaining columns
    """
    
    try:
        # Read the entire file, handling tab-separated values
        data = np.loadtxt(filename, delimiter='\t')
        
        # Extract first column as x-axis values
        x_values = data[:, 0]
        
        # Extract remaining columns as the data matrix
        data_matrix = data[:, 1:] # rows = wavelengths, columns = position
        data_matrix = data_matrix.T # rows = positions, columns = wavelengths
        
        print(f"Successfully loaded data from {filename}")
        print(f"Number of rows (n): {data.shape[0]}")
        print(f"Number of columns (m): {data.shape[1]}")
        print(f"x_values shape: {x_values.shape}")
        print(f"data_matrix shape: {data_matrix.shape}")
        
        return x_values, data_matrix, data_matrix.shape
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except ValueError as e:
        print(f"Error reading file: {e}")
        print("Make sure all values are valid floating-point numbers.")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None
    
x, matrix, shape = read_data_from_txt(filename)