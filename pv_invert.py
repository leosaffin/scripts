import numpy as np
from numpy import pi
import grid
import interpolate
import convert
import pvi

omega = 7.2921e-5 # Coriolis Term
gravity = 9.81    # Gravitational Acceleration
f_0 = 1.e-4       # Typical Coriolis Parameter
ll = 12000        # dy in m
tho = f_0*f_0*ll*ll
laplacian_coefficients = np.zeros((ny,5))
for i in xrange(0,ny):
    laplacian_coefficients[i,0] = 1.0
    laplacian_coefficients[i,1] = 1.0
    laplacian_coefficients[i,2] = -4.0
    laplacian_coefficients[i,3] = 1.0
    laplacian_coefficients[i,4] = 1.0

def pv_invert(pv, boundary_theta, levels=np.arange(50,1000,50), 
              relaxation_parameter=0.4, max_iterations=1999, max_cycles=999,
              omega_s=1.7, omega_h=1.4, thrs1 = 0.1, **kwargs):

    threshold = gravity*thrs1/tho
    [nz,ny,nx] = pv.data.shape
    if 'polelon' in kwargs and 'polelat' in kwargs:
        [lon,lat] = grid.unrotate(pv.coord('grid_longitude').points,
                                  pv.coord('grid_latitude').points,
                                  kwargs['polelon'],kwargs['polelat'])
    else:
        lon = pv.coords('grid_longitude').points()
        lat = pv.coords('grid_latitude').points()
        lon,lat = np.meshgrid(lon,lat)

    coriolis_parameter = 2*omega*np.sin(lat)
    cos_latitude = np.cos(lat)
    [geopotential_height, streamfunction] = first_guess(pv)
    exner = convert.pressure_to_exner(levels)
    pv_in = pv.data 

    [geopotential_height,
     streamfunction,
     pv_out,
     boundary_theta]      = pvi.balnc(coriolis_parameter, cos_latitude,
                                      laplacian_coefficients, 
                                      geopotential_height,
                                      streamfunction, pv_in, boundary_theta, 
                                      exner, relaxation_parameter, threshold, 
                                      max_iterations, max_cycles,
                                      omega_s, omega_h)

    return [geopotential_height,streamfunction]

# Gives a first guess for streamfunction and geopotential height
def first_guess(pv):
    geopotential_height = np.ones(((pv.data.shape)))
    streamfunction = geopotential_height
    return [geopotential_height, streamfunction]
