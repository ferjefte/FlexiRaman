#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:16:49 2023

@author: fernandoaguila
"""

import numpy as np
import matplotlib.pylab as plt

def math_geom_model(xi, wavelen, Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, 
                    yi0, yo0, f1, rot,  f2=100, lines=900, yi=0, m=-1, pix_dim=6.5): # regular case

    
    """
    Fucntions that calculates the simulated conical diffraction spectrum of the neon lamp

    Parameters
    ----------
    xi : array float
        x position on the slit [mm].
    wavelen : float
        wavelength of the refered spectral line [nm].
    Phi : float
        angle betweeen the grooves direction and the \alpha axis [deg].
    phi_d1 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    phi_d2 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    thetai : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    thetae : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    xi0 : float
        x coordinate postion of center of slit [mm].
    xo0 : float
        x coordinate position of the center of the camera sensor [mm].
    yi0 : float
        y coordinate postion of center of slit [mm].
    yo0 : float
        y coordinate position of the center of the camera sensor [mm].
    f1 : float
        focal distance of the TTL2 [mm].
    f2 : float
        focal distance of the TTL3 [mm].
    lines : Int
        number of lines on the slit.
    yi : array float
        y position on the slit [mm].
    m : Int
        order of diffraction.
    pix_dim : float
        size of pixels on camera [um].

    Returns
    -------
    array float
        x postions of the lines on the camera sensor [pixels].
    array float
        y postions of the lines on the camera sensor [pixels].

    """
    
    rot=np.deg2rad(rot)
    #xi0p=xi0*np.cos(rot)+yi0*np.sin(rot)
    #yi0p=-xi0*np.sin(rot)+yi0*np.cos(rot)
    xi=xi*np.cos(rot)
    yi=-xi*np.sin(rot)
    
    d=1/lines
    c1=(m*(wavelen)*1e-6)/d 
    c2=np.arctan( ( xi-xi0 )/f1 )
    c3=np.arctan( ( yi-yi0 )/f1 ) 
    
    
    x=(f2*np.tan( np.arcsin( c1*np.cos( np.deg2rad(Phi) )-np.sin( c2+ np.deg2rad(phi_d1) ) ) - np.deg2rad(phi_d2) ))-xo0 # everything in mm
    y=-(f2*np.tan( np.arcsin( c1*( np.sin( np.deg2rad(Phi) )/np.cos(c2+ np.deg2rad(phi_d1) ) ) - np.sin( c3+ np.deg2rad(thetai) ) ) - np.deg2rad(thetae) ))-yo0 # everything in mm     

    
    x=np.array( x*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    y=np.array( y*1000/pix_dim, dtype='float')+1024 # conversion to pixels

    
    return x, y    # final result in pixels



#%%
def math_geom_model_cuad(xi, wavelen, Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, 
                    yi0, yo0, f1, rot, a, b,  f2=100, lines=900, yi=0, m=-1, pix_dim=6.5): # both terms cubic and quintic

    
    """
    Fucntions that calculates the simulated conical diffraction spectrum of the neon lamp

    Parameters
    ----------
    xi : array float
        x position on the slit [mm].
    wavelen : float
        wavelength of the refered spectral line [nm].
    Phi : float
        angle betweeen the grooves direction and the \alpha axis [deg].
    phi_d1 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    phi_d2 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    thetai : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    thetae : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    xi0 : float
        x coordinate postion of center of slit [mm].
    xo0 : float
        x coordinate position of the center of the camera sensor [mm].
    yi0 : float
        y coordinate postion of center of slit [mm].
    yo0 : float
        y coordinate position of the center of the camera sensor [mm].
    f1 : float
        focal distance of the TTL2 [mm].
    f2 : float
        focal distance of the TTL3 [mm].
    lines : Int
        number of lines on the slit.
    yi : array float
        y position on the slit [mm].
    m : Int
        order of diffraction.
    pix_dim : float
        size of pixels on camera [um].

    Returns
    -------
    array float
        x postions of the lines on the camera sensor [pixels].
    array float
        y postions of the lines on the camera sensor [pixels].

    """
    
    rot=np.deg2rad(rot)
    #xi0p=xi0*np.cos(rot)+yi0*np.sin(rot)
    #yi0p=-xi0*np.sin(rot)+yi0*np.cos(rot)
    xi=xi*np.cos(rot)
    yi=-xi*np.sin(rot)
    
    d=1/lines
    c1=(m*(wavelen)*1e-6)/d 
    c2=np.arctan( ( xi-xi0 )/f1 )
    c3=np.arctan( ( yi-yi0 )/f1 ) 
    
    
    x=(f2*np.tan( np.arcsin( c1*np.cos( np.deg2rad(Phi) )-np.sin( c2+ np.deg2rad(phi_d1) ) ) - np.deg2rad(phi_d2) ))-xo0 # everything in mm
    y=-(f2*np.tan( np.arcsin( c1*( np.sin( np.deg2rad(Phi) )/np.cos(c2+ np.deg2rad(phi_d1) ) ) - np.sin( c3+ np.deg2rad(thetai) ) ) - np.deg2rad(thetae) ))-yo0 # everything in mm     
    
    x= + x + a*(x**2) 
    y= + y + b*(y**2) 
    
    x=np.array( x*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    y=np.array( y*1000/pix_dim, dtype='float')+1024 # conversion to pixels

    
    return x, y    # final result in pixels



#%%
def math_geom_model_cubquint(xi, wavelen, Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, 
                    yi0, yo0, f1, rot, a1, a2, b1, b2,  f2=100, lines=900, yi=0, m=-1, pix_dim=6.5): # both terms cubic and quintic

    
    """
    Fucntions that calculates the simulated conical diffraction spectrum of the neon lamp

    Parameters
    ----------
    xi : array float
        x position on the slit [mm].
    wavelen : float
        wavelength of the refered spectral line [nm].
    Phi : float
        angle betweeen the grooves direction and the \alpha axis [deg].
    phi_d1 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    phi_d2 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    thetai : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    thetae : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    xi0 : float
        x coordinate postion of center of slit [mm].
    xo0 : float
        x coordinate position of the center of the camera sensor [mm].
    yi0 : float
        y coordinate postion of center of slit [mm].
    yo0 : float
        y coordinate position of the center of the camera sensor [mm].
    f1 : float
        focal distance of the TTL2 [mm].
    f2 : float
        focal distance of the TTL3 [mm].
    lines : Int
        number of lines on the slit.
    yi : array float
        y position on the slit [mm].
    m : Int
        order of diffraction.
    pix_dim : float
        size of pixels on camera [um].

    Returns
    -------
    array float
        x postions of the lines on the camera sensor [pixels].
    array float
        y postions of the lines on the camera sensor [pixels].

    """
    
    rot=np.deg2rad(rot)
    #xi0p=xi0*np.cos(rot)+yi0*np.sin(rot)
    #yi0p=-xi0*np.sin(rot)+yi0*np.cos(rot)
    xi=xi*np.cos(rot)
    yi=-xi*np.sin(rot)
    
    d=1/lines
    c1=(m*(wavelen)*1e-6)/d 
    c2=np.arctan( ( xi-xi0 )/f1 )
    c3=np.arctan( ( yi-yi0 )/f1 ) 
    
    
    x=(f2*np.tan( np.arcsin( c1*np.cos( np.deg2rad(Phi) )-np.sin( c2+ np.deg2rad(phi_d1) ) ) - np.deg2rad(phi_d2) ))-xo0 # everything in mm
    y=-(f2*np.tan( np.arcsin( c1*( np.sin( np.deg2rad(Phi) )/np.cos(c2+ np.deg2rad(phi_d1) ) ) - np.sin( c3+ np.deg2rad(thetai) ) ) - np.deg2rad(thetae) ))-yo0 # everything in mm     
    
    x=  x + a1*(x**2) + a2*(x**4)
    y=  y + b1*(y**2) + b2*(y**4)
    
    x=np.array( x*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    y=np.array( y*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    
    
    # print('x:', x)
    # print('y:', y)
    
    return x, y    # final result in pixels



#%%
def math_geom_model_seventh(xi, wavelen, Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, 
                    yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6, f2=100, lines=900, yi=0, m=-1, pix_dim=6.5): # both terms cubic and quintic

    
    """
    Fucntions that calculates the simulated conical diffraction spectrum of the neon lamp

    Parameters
    ----------
    xi : array float
        x position on the slit [mm].
    wavelen : float
        wavelength of the refered spectral line [nm].
    Phi : float
        angle betweeen the grooves direction and the \alpha axis [deg].
    phi_d1 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    phi_d2 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    thetai : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    thetae : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    xi0 : float
        x coordinate postion of center of slit [mm].
    xo0 : float
        x coordinate position of the center of the camera sensor [mm].
    yi0 : float
        y coordinate postion of center of slit [mm].
    yo0 : float
        y coordinate position of the center of the camera sensor [mm].
    f1 : float
        focal distance of the TTL2 [mm].
    f2 : float
        focal distance of the TTL3 [mm].
    lines : Int
        number of lines on the slit.
    yi : array float
        y position on the slit [mm].
    m : Int
        order of diffraction.
    pix_dim : float
        size of pixels on camera [um].

    Returns
    -------
    array float
        x postions of the lines on the camera sensor [pixels].
    array float
        y postions of the lines on the camera sensor [pixels].

    """
    
    rot=np.deg2rad(rot)
    #xi0p=xi0*np.cos(rot)+yi0*np.sin(rot)
    #yi0p=-xi0*np.sin(rot)+yi0*np.cos(rot)
    xi=xi*np.cos(rot)
    yi=-xi*np.sin(rot)
    
    d=1/lines
    c1=(m*(wavelen)*1e-6)/d 
    c2=np.arctan( ( xi-xi0 )/f1 )
    c3=np.arctan( ( yi-yi0 )/f1 ) 
    
    
    x=(f2*np.tan( np.arcsin( c1*np.cos( np.deg2rad(Phi) )-np.sin( c2+ np.deg2rad(phi_d1) ) ) - np.deg2rad(phi_d2) ))-xo0 # everything in mm
    y=-(f2*np.tan( np.arcsin( c1*( np.sin( np.deg2rad(Phi) )/np.cos(c2+ np.deg2rad(phi_d1) ) ) - np.sin( c3+ np.deg2rad(thetai) ) ) - np.deg2rad(thetae) ))-yo0 # everything in mm     
    
    
    r=np.sqrt(x**2+y**2)
    angle=np.arctan2(x,y)
    
    
    y_sim= ( r + a1*(r**2) + a2*(r**3) + a3*(r**4) + a4*(r**5) + a5*(r**6) + a6*(r**7) ) * np.cos(angle)
    x_sim= ( r + a1*(r**2) + a2*(r**3) + a3*(r**4) + a4*(r**5) + a5*(r**6) + a6*(r**7) ) * np.sin(angle)
    
    x_pix=np.array( x_sim*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    y_pix=np.array( y_sim*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    

    
    return x_pix, y_pix    # final result in pixels


#%%
def math_geom_model_seventh_centershift(xi, wavelen, Phi, phi_d1, phi_d2, thetai, thetae, xi0, xo0, 
                    yi0, yo0, f1, rot, a1, a2, a3, a4, a5, a6, Px0p, Py0p, f2=100, lines=900, yi=0, m=-1, pix_dim=6.5): # both terms cubic and quintic

    
    """
    Fucntions that calculates the simulated conical diffraction spectrum of the neon lamp

    Parameters
    ----------
    xi : array float
        x position on the slit [mm].
    wavelen : float
        wavelength of the refered spectral line [nm].
    Phi : float
        angle betweeen the grooves direction and the \alpha axis [deg].
    phi_d1 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    phi_d2 : float
        angle in xz plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    thetai : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL2 [deg].
    thetae : float
        angle in xy plane between the gratting normal and the normal of the tube lens TTL3 [deg].
    xi0 : float
        x coordinate postion of center of slit [mm].
    xo0 : float
        x coordinate position of the center of the camera sensor [mm].
    yi0 : float
        y coordinate postion of center of slit [mm].
    yo0 : float
        y coordinate position of the center of the camera sensor [mm].
    f1 : float
        focal distance of the TTL2 [mm].
    f2 : float
        focal distance of the TTL3 [mm].
    lines : Int
        number of lines on the slit.
    yi : array float
        y position on the slit [mm].
    m : Int
        order of diffraction.
    pix_dim : float
        size of pixels on camera [um].

    Returns
    -------
    array float
        x postions of the lines on the camera sensor [pixels].
    array float
        y postions of the lines on the camera sensor [pixels].

    """
    
    rot=np.deg2rad(rot)
    #xi0p=xi0*np.cos(rot)+yi0*np.sin(rot)
    #yi0p=-xi0*np.sin(rot)+yi0*np.cos(rot)
    xi=xi*np.cos(rot)
    yi=-xi*np.sin(rot)
    
    d=1/lines
    c1=(m*(wavelen)*1e-6)/d 
    c2=np.arctan( ( xi-xi0 )/f1 )
    c3=np.arctan( ( yi-yi0 )/f1 ) 
    
    
    x=(f2*np.tan( np.arcsin( c1*np.cos( np.deg2rad(Phi) )-np.sin( c2+ np.deg2rad(phi_d1) ) ) - np.deg2rad(phi_d2) ))-xo0 # everything in mm
    y=-(f2*np.tan( np.arcsin( c1*( np.sin( np.deg2rad(Phi) )/np.cos(c2+ np.deg2rad(phi_d1) ) ) - np.sin( c3+ np.deg2rad(thetai) ) ) - np.deg2rad(thetae) ))-yo0 # everything in mm     
    
    
    r=np.sqrt((x-Px0p)**2+(y-Py0p)**2)
    angle=np.arctan2(x-Px0p,y-Py0p)
    
    
    y_sim= ( r + a1*(r**2) + a2*(r**3) + a3*(r**4) + a4*(r**5) + a5*(r**6) + a6*(r**7) ) * np.cos(angle) + Py0p
    x_sim= ( r + a1*(r**2) + a2*(r**3) + a3*(r**4) + a4*(r**5) + a5*(r**6) + a6*(r**7) ) * np.sin(angle) + Px0p
    
    x_pix=np.array( x_sim*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    y_pix=np.array( y_sim*1000/pix_dim, dtype='float')+1024 # conversion to pixels
    

    
    return x_pix, y_pix    # final result in pixels