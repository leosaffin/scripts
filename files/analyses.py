"""
Start by running the script conv2nc.tcl on the raw analyses
"""

import iris
from iris.cube import CubeList
from iris.util import squeeze
from mymodule import interpolate

name_pairs = [('DENSITY*R*R AFTER TIMESTEP', 'air_density'),
              ('eastward_wind', 'x_wind'),
              ('northward_wind', 'y_wind')]

units = [('air_density', 'kg m-3'),
         ('dimensionless_exner_function', '1'),
         ('mass_fraction_of_cloud_ice_in_air', '1'),
         ('mass_fraction_of_cloud_liquid_water_in_air', '1')]

file_pairs = [('', ''),
              ('', '')]


def main():
    path = '/projects/diamet/lsaffi/iop8/'

    basis_cube = iris.load_cube(path + 'prognostics_001.nc')

    for infile, outfile in file_pairs:
        cubes = iris.load(path + infile)
        newcubes = redo_cubes(cubes, basis_cube)
        iris.save(newcubes, path + outfile)


def redo_cubes(cubes, basis_cube):
    # Coordinates to copy to analyses
    z = basis_cube.coord('level_height')
    lat = basis_cube.coord('grid_latitude')
    lon = basis_cube.coord('grid_longitude')
    sigma = basis_cube.coord('sigma')
    surf = basis_cube.coord('surface_altitude')

    newcubelist = CubeList()
    for cube in cubes:
        # Squeeze cubes dimensions
        newcube = squeeze(cube)

        # Give time coordinate proper name
        newcube.coord('t').rename('time')

        # Remap the cubes to theta points
        newcube.coord('Hybrid height').rename('level_height')
        newcube.coord('grid_latitude').coord_system = lat.coord_system
        newcube.coord('grid_longitude').coord_system = lon.coord_system
        newcube = interpolate.remap_3d(newcube, basis_cube, 'level_height')

        # Give the cube the standard coordinates
        for coord in (z, lat, lon):
            newcube.replace_coord(coord)

        # Add extra auxiliary coordinates
        newcube.add_aux_coord(sigma, 0)
        newcube.add_aux_coord(surf, [1, 2])

        newcubelist.append(newcube)

    # Correct cube names
    for before, after in name_pairs:
        newcubelist.extract(before)[0].rename(after)

    # Correct units
    for name, unit in units:
        newcubelist.extract(name)[0].units = unit

    return newcubelist
