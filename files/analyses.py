"""
Start by running the script conv2nc.tcl on the raw analyses from the xcm
"""

import iris
from iris.cube import CubeList
from iris.util import squeeze
from mymodule import convert, interpolate

# Define which area of grid to subset
slices = slice(0, 50), slice(15, 345), slice(15, 585)

# Define how to rename variables
name_pairs = [('DENSITY*R*R AFTER TIMESTEP', 'air_density'),
              ('eastward_wind', 'x_wind'),
              ('northward_wind', 'y_wind')]

# Correct units for some cubes
units = [('air_density', 'kg m-3'), q
         ('dimensionless_exner_function', '1'),
         ('mass_fraction_of_cloud_ice_in_air', '1'),
         ('mass_fraction_of_cloud_liquid_water_in_air', '1')]

path = '/projects/diamet/lsaffi/iop5/'
file_pairs = [(path + '20111129_qwqy12.nc', path + 'analysis_024.nc')]


def main():
    basis_cube = iris.load_cube(path + 'prognostics_001.nc',
                                'air_potential_temperature')
    basis_cube.remove_coord('forecast_reference_time')
    basis_cube.remove_coord('forecast_period')

    for infile, outfile in file_pairs:
        cubes = iris.load(infile)
        newcubes = redo_cubes(cubes, basis_cube)
        iris.save(newcubes, outfile)


def redo_cubes(cubes, basis_cube):
    # Coordinates to copy to analyses
    z = basis_cube.coord('level_height')
    lat = basis_cube.coord('grid_latitude')
    lon = basis_cube.coord('grid_longitude')
    sigma = basis_cube.coord('sigma')
    surf = basis_cube.coord('surface_altitude')
    altitude = basis_cube.coord('altitude')

    newcubelist = CubeList()
    for cube in cubes:
        # Squeeze cubes dimensions
        newcube = squeeze(cube)
        newcube = newcube[slices]

        # Give time coordinate proper name
        newcube.coord('t').rename('time')

        # Remap the cubes to theta points
        newcube.coord('Hybrid height').rename(z.name())
        newcube.coord('grid_latitude').coord_system = lat.coord_system
        newcube.coord('grid_longitude').coord_system = lon.coord_system
        newcube = interpolate.remap_3d(newcube, basis_cube, 'level_height')

        # Give the cube the standard coordinates
        for n, coord in enumerate([z, lat, lon]):
            newcube.remove_coord(coord.name())
            newcube.add_dim_coord(coord, n)

        # Add extra auxiliary coordinates
        newcube.add_aux_coord(sigma, 0)
        newcube.add_aux_coord(surf, [1, 2])
        newcube.add_aux_coord(altitude, [0, 1, 2])

        newcubelist.append(newcube)

    # Correct cube names
    for before, after in name_pairs:
        newcubelist.extract(before)[0].rename(after)

    # Convert density to true density
    rho = convert.calc('air_density', cubes)
    z = rho.coord('altitude')
    r = z.data + convert.r.data
    rho.data = rho.data / r ** 2

    # Correct units
    for name, unit in units:
        newcubelist.extract(name)[0].units = unit

    return newcubelist

if __name__ == '__main__':
    main()
