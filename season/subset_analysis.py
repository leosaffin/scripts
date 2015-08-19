"""Replaces an analysis with a .pp file with a subset of cubes
"""

import glob
import numpy as np
import iris
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
         'surface_altitude',
         'atmosphere_boundary_layer_thickness',
         'surface_altitude',
         'short_wave_radiation_pv',
         'long_wave_radiation_pv',
         'microphysics_pv',
         'gravity_wave_drag_pv',
         'convection_pv',
         'boundary_layer_pv',
         'advection_inconsistency_pv',
         'cloud_rebalancing_pv']


def main():
    """ Modifies all .analysis files in the current directory
    """
    for analysis_file in glob.glob('*.analysis'):
        output_file = analysis_file + '.pp'
        newpp(analysis_file, output_file)


def newpp(analysis_file, output_file):
    """ Copies an analysis file taking a subset of variables
    """
    cubelist = files.load(analysis_file)
    newcubelist = iris.cube.CubeList()

    for name in names:
        cube = convert.calc(name, cubelist)
        cube = cube[zmin:zmax, ymin:ymax, xmin:xmax]
        newcubelist.append(cube)

    # Calculate diagnostic variables
    u = convert.calc('x_wind', cubelist)
    v = convert.calc('y_wind', cubelist)
    w = convert.calc('upward_air_velocity', cubelist)
    theta = convert.calc('air_potential_temperature', cubelist)
    rho_rsq = convert.calc('air_density_times_r_squared', cubelist)
    Pi = convert.calc('dimensionless_exner_function', cubelist)

    # y_wind
    newcubelist.append(v[zmin:zmax, (ymin - 1):(ymax - 1), xmin:xmax])

    # upward_air_velocity
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
    newcubelist.append(cube[zmin:zmax, ymin:ymax, xmin:xmax])

    # Air pressure on rho levels
    P_rho = convert.calc('air_pressure', cubelist)
    P_rho.attributes['STASH'] = STASH()
    newcubelist.append(P_rho[zmin:zmax, ymin:ymax, xmin:xmax])

    # Air pressure on theta levels
    P_theta = interpolate.main(
        P_rho, level_height=theta.coord('level_height').points)
    P_theta.attributes['STASH'] = STASH()
    newcubelist.append(P_theta[zmin:zmax, ymin:ymax, xmin:xmax])

    # Surface pressure
    P_surf = interpolate.main(
        P_rho, level_height=theta.coord('level_height').points)[0]
    P_surf.attributes['STASH'] = STASH()
    newcubelist.append(P_surf[zmin:zmax, ymin:ymax, xmin:xmax])

    # Air temperature
    T = convert.temp(P_theta, theta)
    T.attributes['STASH'] = STASH(1, 16, 4)
    newcubelist.append(T[zmin:zmax, ymin:ymax, xmin:xmax])

    # Convective rainfall amount
    data = np.zeros([zmax - zmin, ymax - ymin, xmax - xmin])
    cube = iris.cube.Cube(data)
    cube.attributes['STASH'] = STASH(1, 5, 201)
    newcubelist.append(cube)

    # Stratiform rainfall amount
    cube = iris.cube.Cube(data)
    cube.attributes['STASH'] = STASH(1, 4, 201)
    newcubelist.append(cube)

    files.save(newcubelist, output_file)

    return


if __name__ == '__main__':
    main()
