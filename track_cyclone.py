"""Find a cyclone track by the successive nearest minima in sea-level pressure
   starting from a user defined start point
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import filters
import iris
from mymodule import grid, plot
from mymodule.user_variables import datadir


def main():
    job = 'iop8'
    # Load sea level pressure map at all times
    mslp = iris.load_cube(datadir + job + '/diagnostics_*.nc',
                          'air_pressure_at_sea_level')
    mslp.convert_units('hPa')
    
    # Track pressure minima from custom start point
    idx_0 = 220, 127
    track, indices = track_position(mslp, idx_0)
    
    # Save track data
    np.save(datadir + job + '/cyclone_track.npy', track)
    np.save(datadir + job + '/cyclone_track_indices.npy', indices)
    
    # Track mslp following the cyclone
    mslp_track = track_variable(mslp, indices)
    np.save(datadir + job + '/cyclone_mslp.npy', mslp_track)
    
    return


def track_position(mslp, idx_0):
    # Set the start point of the cyclone manually
    lon, lat = grid.get_xy_grids(mslp)
    current_x, current_y = lon[idx_0], lat[idx_0]

    nt = mslp.shape[0]
    track = [[current_x-360, current_y]]
    indices = [idx_0]
    
    # Take the nearest local minima in sea-level pressure at each timestep
    for n in range(nt):
        print n
        local_minima = find_local_minima(mslp[n].data)        
        new_x, new_y, idx = find_nearest_minima(current_x, current_y,
                                                local_minima, lon, lat)
        
        track.append([new_x-360, new_y])
        indices.append(idx)
        current_x, current_y = new_x, new_y

    # Save the data as a numpy array s   
    track = np.array(track)
    indices = np.array(indices)
    
    return track, indices
    

def plot_track(mslp, track):
    # Show the track
    cs = plot.contour(mslp[-1], range(950, 1050, 5), colors='k')
    plt.clabel(cs, fmt='%1.0f')
    plt.plot(track[:, 0], track[:, 1], '-rx')

    return


def find_local_minima(array):
    # Get the minimum values within a set number of gridpoints
    array_min = filters.minimum_filter(array, size=10)
    
    # Local minima where the gridpoint matches the area minimum
    local_minima = np.where(array == array_min)
    
    return local_minima

def find_local_maxima(array):
    # Get the minimum values within a set number of gridpoints
    array_max = filters.maximum_filter(array, size=10)
    
    # Local minima where the gridpoint matches the area minimum
    local_maxima = np.where(array == array_max)
    
    return local_maxima

def find_nearest_minima(x, y, local_minima, lon, lat):
    current_minimum_distance = 1e10
    
    # Calculate the distance to each of the local minima
    for n in range(len(local_minima[0])):
        dlambda = x - lon[local_minima][n]
        dphi = y - lat[local_minima][n]
        distance = np.sqrt(dphi**2 + dlambda**2)
        
        # Take the shortest distance
        if distance < current_minimum_distance:
            new_x = lon[local_minima][n]
            new_y = lat[local_minima][n]
            idx = local_minima[0][n], local_minima[1][n]
            current_minimum_distance = distance
            
    return new_x, new_y, idx


def track_variable(cube, idx, name):
    variable = []
    nt = cube.shape[0]
    for n in range(nt):
        print n
        variable.append(cube.data[n, idx[n][0], idx[n][1]])

    return variable

if __name__=='__main__':
    main()
    
