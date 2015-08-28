"""Replaces an analysis with a .pp file with a subset of cubes
"""

import glob
import os
import numpy as np
import iris
from iris.unit import Unit
from iris.fileformats.pp import STASH
from mymodule import files, convert, interpolate, variable


# Subset of dimensions to extract
zmin = 0
zmax = 50
ymin = 15
ymax = 345
xmin = 15
xmax = 585

# List of variables to extract from the analysis
names = ['x_wind',
         'specific_humidity',
         'mass_fraction_of_cloud_liquid_water_in_air',
         'mass_fraction_of_cloud_ice_in_air',
         'short_wave_radiation_pv',
         'long_wave_radiation_pv',
         'microphysics_pv',
         'gravity_wave_drag_pv',
         'convection_pv',
         'boundary_layer_pv',
         'advection_inconsistency_pv',
         'cloud_rebalancing_pv']


def main(url):
    """ Modifies all .analysis files in the current directory
    """
    for analysis_file in glob.glob(url + '*.analysis'):
        try:
            output_file = analysis_file + '.pp'
            newpp(analysis_file, output_file)
        except ValueError:
            print('Could not subset ' + analysis_file)


def newpp(analysis_file, output_file):
    """ Copies an analysis file taking a subset of variables
    """
    print analysis_file
    cubelist = files.load(analysis_file)
    newcubelist = iris.cube.CubeList()

    for name in names:
        cube = convert.calc(name, cubelist)
        newcubelist.append(cube[zmin:zmax, ymin:ymax, xmin:xmax])

    # Calculate diagnostic variables
    u = convert.calc('x_wind', cubelist)
    v = convert.calc('y_wind', cubelist)
    w = convert.calc('upward_air_velocity', cubelist)
    theta = convert.calc('air_potential_temperature', cubelist)
    rho_rsq = convert.calc('air_density_times_r_squared', cubelist)
    Pi = convert.calc('dimensionless_exner_function', cubelist)

    # Surface altitude
    surf = convert.calc('surface_altitude', cubelist)
    newcubelist.append(surf[ymin:ymax, xmin:xmax])
    newcubelist.append(surf[ymin:ymax, xmin:xmax])

    # Atmosphere boundary layer thickness
    bl = convert.calc('atmosphere_boundary_layer_thickness', cubelist)
    newcubelist.append(bl[ymin:ymax, xmin:xmax])

    # Meridional velocity
    newcubelist.append(v[zmin:zmax, (ymin - 1):(ymax - 1), xmin:xmax])

    # Vertical velocity
    newcubelist.append(w[(zmin + 1):(zmax + 1), ymin:ymax, xmin:xmax])

    # Advection only PV
    pv = variable.pv(u, v, w, theta, rho_rsq)
    cube = convert.calc('advection_only_pv', cubelist)
    cube = cube.copy(data=pv.data)
    newcubelist.append(cube[zmin:zmax, ymin:ymax, xmin:xmax])

    # Total PV
    cube = convert.calc('total_pv', cubelist)
    cube = cube.copy(data=pv.data)
    newcubelist.append(cube[zmin:zmax, ymin:ymax, xmin:xmax])

    # Mean sea-level pressure
    cube = variable.mslp(theta, Pi, w)
    cube.attributes['STASH'] = STASH(1, 16, 222)
    newcubelist.append(cube[ymin:ymax, xmin:xmax])

    # Air pressure on rho levels
    P_rho = convert.calc('air_pressure', cubelist)
    P_rho.attributes['STASH'] = STASH(1, 0, 407)
    P_rho.rename('air_pressure')
    newcubelist.append(P_rho[zmin:zmax, ymin:ymax, xmin:xmax])

    # Air pressure on theta levels
    Pi_theta = interpolate.main(
        Pi, level_height=theta.coord('level_height').points)
    # Interpolated cubes muck up pp saver
    Pi_theta = theta.copy(data=Pi_theta.data)
    Pi_theta.rename('dimensionless_exner_function')
    Pi_theta.units = Unit('')

    # Air pressure on theta levels
    P_theta = convert.pressure(Pi_theta)
    P_theta.attributes['STASH'] = STASH(1, 0, 408)
    P_theta.rename('air_pressure')
    newcubelist.append(P_theta[zmin:zmax, ymin:ymax, xmin:xmax])

    # Surface pressure
    P_surf = interpolate.main(
        P_rho, level_height=w.coord('level_height').points)[0]
    P_surf.attributes['STASH'] = STASH(1, 0, 409)
    P_surf.rename('surface_air_pressure')
    newcubelist.append(P_surf[ymin:ymax, xmin:xmax])

    # Air temperature
    T = convert.temp(Pi_theta, theta)
    T.attributes['STASH'] = STASH(1, 16, 4)
    T.rename('air_temperature')
    newcubelist.append(T[zmin:zmax, ymin:ymax, xmin:xmax])

    # Convective rainfall amount
    data = np.zeros([ymax - ymin, xmax - xmin])
    cube = surf[ymin:ymax, xmin:xmax].copy(data=data)
    cube.attributes['STASH'] = STASH(1, 5, 201)
    newcubelist.append(cube)

    # Stratiform rainfall amount
    cube = surf[ymin:ymax, xmin:xmax].copy(data=data)
    cube.attributes['STASH'] = STASH(1, 4, 201)
    newcubelist.append(cube)

    files.save(newcubelist, output_file)

    os.system('rm ' + analysis_file)

    return


if __name__ == '__main__':
    url = '/projects/diamet/lsaffi/season/'
    main(url)
