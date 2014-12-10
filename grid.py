a = 6378100
import numpy as np
import fgrid
from math import pi

# Calculate the volume of grid boxes
def volume(cube):
    rho = a + cube.coord('altitude').points
    bounds = a + cube.coord('altitude').bounds
    theta = cube.coord('grid_longitude').points*(np.pi/180)
    phi = (90 - cube.coord('grid_latitude').points)*(np.pi/180)
    return fgrid.volume(rho,bounds,theta,phi)

def volume_global(cube):
    rho = a + cube.coord('altitude').points
    bounds = a + cube.coord('altitude').bounds
    theta = cube.coord('longitude').points*(np.pi/180)
    phi = (90 - cube.coord('latitude').points)*(np.pi/180)
    return fgrid.volume(rho,bounds,theta,phi)

def grad(cube):
    rho = a + cube.coord('altitude').points
    theta = cube.coord('longitude').points*(np.pi/180)
    phi = (90 - cube.coord('latitude').points)*(np.pi/180)
    return fgrid.grad(cube.data,rho,theta,phi)

# Calculate latitude and longitue in rotated system
def rotate(x,y,polelon,polelat):
    # Convert to Radians
    factor = pi/180
    x = factor*x
    y = factor*y
    polelon = factor*polelon
    polelat = factor*polelat
    sin_phi_pole = np.sin(polelat)
    cos_phi_pole = np.cos(polelat)
    if x>pi: 
        x = x - 2*pi

    # Calculate Rotated Latitude
    yr = np.arcsin(cos_phi_pole*np.cos(y)*np.cos(x-polelon) + 
                   sin_phi_pole*np.sin(y))/factor

    # Calculate Rotated Longitude
    arg1 = -np.sin(x-polelon)*np.cos(y)
    arg2 = -sin_phi_pole*np.cos(y)*np.cos(x-polelon) + cos_phi_pole*np.sin(y)
    if np.abs(arg2) < 1e-30:
        if np.abs(arg1) < 1e-30:
            xr = 0.0
        elif arg1>0:
            xr = 90.0
        else:
            xr = -90.0
    else:
        xr = np.arctan2(arg1,arg2)/factor
    return [xr,yr]

#Calculate actual Latitude and Longitude of rotated gridpoints
def unrotate(x,y,polelon,polelat):
    if (polelat>=0):
        sin_phi_pole = np.sin(pi/180*polelat)
        cos_phi_pole = np.cos(pi/180*polelat)
    else:
        sin_phi_pole = -np.sin(pi/180*polelat)
        cos_phi_pole = -np.cos(pi/180*polelat)

    Nx = np.size(x)
    Ny = np.size(y)
    x_p = np.zeros((Nx,Ny))
    y_p = np.zeros((Nx,Ny))

    #convert to radians
    x=(pi/180)*x
    y=(pi/180)*y
    sign = np.sign(x-2*pi)

    #Scale between +/- pi
    x = ((x + pi)%(2*pi)) - pi

    #Compute latitude using equation (4.7)
    arg = (np.outer(np.cos(x),np.cos(y))*cos_phi_pole +
           np.outer(np.ones(Nx),np.sin(y))*sin_phi_pole)
    np.clip(arg,-1,1)
    a_phi = np.arcsin(arg)
    y_p = (180/pi)*a_phi
                                                                            
    #Compute longitude using equation (4.8)
    term1 = (np.outer(np.cos(x),np.cos(y))*sin_phi_pole -
             np.outer(np.ones(Nx),np.sin(y))*cos_phi_pole)
    term2 = np.cos(a_phi)
    a_lambda = np.zeros((Nx,Ny))
    for i in xrange(0,Nx):
        for j in xrange(0,Ny):
            if(abs(term2[i,j])<1e-5):
                a_lambda[i,j]=0.0
            else:
                arg = term1[i,j]/term2[i,j]
                arg = min(arg, 1.0)
                arg = max(arg,-1.0)
                a_lambda[i,j] = (180/pi)*np.arccos(arg)
                a_lambda[i,j] = a_lambda[i,j]*sign[i]
    x_p = a_lambda + polelon - 180
    return [x_p,y_p]

#Specify heights of theta points for terrain following coordinates 
def true_height(h,zp,k_flat):
    nz = np.size(zp)
    size = h.shape
    z = np.zeros(((nz,size[0],size[1])))
    eta = zp/zp[nz-1]
    eta_i = eta[k_flat]
    for k in xrange(0,nz):
        z[k,:,:] = eta[k] * zp[nz-1]
    for k in xrange(0,k_flat):
        z[k,:,:] += h*((1-(eta[k]/eta_i))**2)
    return z

