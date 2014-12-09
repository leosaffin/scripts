import numpy as np
from numpy import pi
import grid
import interpolate
import convert

import pvi
omega = 7.2921e-5 # Coriolis Term
gravity = 9.81    # Gravitational Acceleration
f_0 = 1.e-4        # Typical Coriolis Parameter

def pv_invert(pv, boundary_theta, levels=np.arange(1000,50,50), 
              relaxation_parameter=0.4, max_iterations=1999, max_cycles=999,
              omega_s=1.7, omega_h=1.4, thrs1 = 0.1, **kwargs):
    #zhdr_5 = longitude resolution
    ll = 2.e7*zhdr_5 /180.  #dy in m
    tho = f_0*f_0*ll*ll
    threshold = gravity*thrs1/tho
    #laplacian_coefficients =

    if polelon in kwargs and polelat in kwargs:
        [longitude,latitude] = grid.unrotate(
                                pv.coords('grid_longitude').points(),
                                pv.coords('grid_latitude').points(),
                                kwargs['polelon'],kwargs['polelat'])
    else:
        longitude = pv.coords('grid_longitude').points()
        latitude = pv.coords('grid_latitude').points()
    coriolis_parameter = 2*omega*np.sin(latitude)
    cos_latitude = np.cos(latitude)
    [geopotential_height, streamfunction] = first_guess()
    exner = convert.pressure_to_exner(levels)

    [geopotential_height,
     streamfunction,
     pv.data,
     boundary_theta]      = pvi.balnc(coriolis_parameter, cos_latitude,
                                      laplacian_coefficients, 
                                      geopotential_height,
                                      streamfunction, pv.data, boundary_theta, 
                                      exner, relaxation_parameter, threshold, 
                                      max_iterations, max_cycles,
                                      omega_s, omega_h)

     return [geopotential_height,streamfunction]

# Gives a first guess for streamfunction and geopotential height
def first_guess()
