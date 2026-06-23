# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:37:23 2026

Script to analyse what happens to the Power distribution when using a Bessel beam

According to Cizmar thesis, for on axis intensity:
    
    I(\ro=0, z)= ( I_0*2*\pi*k*z )/( cos(\alpha_0) ) * sin(\alpha_0)**2 * exp( -2 * ( ( z*tan(\alpha_0) )/( \omega_0 ) )**2 )
    
for on vicinity of z-axis:
    
    I(\ro, z)= ( I_0*pi*k*sin(\alpha_0)/2 ) * [ ( F1+F2 )**2 * J_0( k*\ro*sin(\alpha_0) )**2 + ( F1-F2 )**2 * J_1( k*\ro*sin(\alpha_0) )**2 ] 
    
with:
    
    F1 = \sqrt( z*tan(\alpha_0)+\ro ) * exp( -( ( z*tan(\alpha_0)+\ro )/( \omega_0 ) )**2 )
    
    F2 = \sqrt( z*tan(\alpha_0)-\ro ) * exp( -( ( z*tan(\alpha_0)-\ro )/( \omega_0 ) )**2 ) * H(z*tan(\alpha_0)-\ro)
    
where:
    
    H = 1 for z*tan(\alpha_0) >= \ro
    H = 0 z*tan(\alpha_0) < \ro
    
@author: aguilafernando
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.special import j0, j1
from pathlib import Path

# Define an array of Z
z = np.linspace(0, 200, 100, endpoint=True) # [mm]
z_max = 9.1 # where the max intensity happens
# z_max = 1
# Define constants
k = 11814.04185 # [1/mm]
alphas_0 = [0.004028068, 0.00805724, 0.016123321, 0.040464057] # rad
label_alphas = ['0.23°', '0.46° and w_0 = 0.39', '0.92°', '2.3°']
omega_0 = 0.75 # [mm]  
I_0 = 1
ro = np.linspace(0, 0.3, 100) #[mm]



# Define function

def intensity(z, k, alpha_0, omega_0, I_0):
    exp_arg = -2 * ( ( z*np.tan(alpha_0) )/( omega_0 ) )**2
    I = I_0 * ( np.sin(alpha_0) )**2 * ( 2*np.pi*k*z )/( np.cos(alpha_0) ) * np.exp(exp_arg)
    
    return I

# Plotting

fig, ax = plt.subplots(1,1)

for i in range(len(alphas_0)):
    I_r = intensity(z, k, alphas_0[i], omega_0, I_0)
    ax.plot(z, I_r, '--o', label=label_alphas[i])
    ax.set_xlabel('z [mm]')
    ax.set_ylabel('Intensity')
    ax.legend()
    
# saving plot
project_folder = Path(__file__).parent.parent
plot_z_path = os.path.join(project_folder, "data_presentation", "Intensity_z.png")
plt.savefig(plot_z_path, format="png", dpi=300)
    
#%%

# CASE FOR INTENSITY IN THE VICINITY OF Z-AXIS

def F1(ro, z, alpha_0, omega_0):
    a = z*np.tan(alpha_0) + ro
    exp_arg = a/omega_0
    return np.sqrt(a) * np.exp( -np.power(exp_arg ,2) )

def F2(ro, z, alpha_0, omega_0):
    a = z*np.tan(alpha_0)
    b = a - ro
    exp_arg = b/omega_0
    
    if a >= ro:
        return np.sqrt(b) * np.exp( -np.power(exp_arg ,2) )
    elif a < ro:
        return  0
    
def intensity_ro(z, k, alpha_0, omega_0, I_0, ro):
    f1 = F1(ro, z, alpha_0, omega_0)
    f2 = F2(ro, z, alpha_0, omega_0)
    j0_arg = k * ro * np.sin(alpha_0)
    a = np.power( (f1+f2), 2) * np.power( j0( j0_arg ), 2)
    b = np.power( (f1-f2), 2) * np.power( j1( j0_arg ), 2)
    
    return ( ( I_0*np.pi*k*np.sin(alpha_0) )/2 ) * ( a + b )

# Plotting

zs = [z_max, 23.26, 46.6, 94]

for l in zs:
    fig, ax = plt.subplots(1,1)
    
    
    for j in range(len(alphas_0)):
        I_ro_arr = []
        for i in ro:
            I_ro = intensity_ro(l, k, alphas_0[j], omega_0, I_0, i)
            I_ro_arr.append(I_ro)
        ax.plot(ro, I_ro_arr, '--o', label=label_alphas[j] )
        
    ax.set_xlabel('ro [mm]')
    ax.set_ylabel('Intensity')
    ax.set_title(f'Intensity along ro for z = {l} mm')
    ax.legend()
    
    plot_ro_path = os.path.join(project_folder, "data_presentation", f"Intensity_ro_z_{l}.png")
    plt.savefig(plot_ro_path, format="png", dpi=300)
        
# fig, ax = plt.subplots(1,1)
# arg = np.linspace(0,10, 50)
# ax.plot(arg,  np.power( j0( arg ), 2))
# ax.plot(arg,  np.power( j1( arg ), 2))