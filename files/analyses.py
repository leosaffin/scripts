"""
Start by running the script conv2nc.tcl on the raw analyses from the xcm
"""

import iris
from mymodule import convert, grid
import files

# Filename parameters
path = '/projects/diamet/lsaffi/'
time = 'hours since 2011-11-28 12:00:00'
file_pairs = [(path + '/iop5/20111129_qwqy12.nc',
               path + 'temp/analysis_024.nc')]

# Define which area of grid to subset
slices = slice(0, 50), slice(15, 345), slice(15, 585)

# Load basis cube
basis_cube = iris.load_cube(path + 'temp/prognostics_001.nc',
                            'air_potential_temperature')
lat = grid.extract_dim_coord(basis_cube, 'y')
lon = grid.extract_dim_coord(basis_cube, 'x')

# Define how to rename variables
name_pairs = [('DENSITY*R*R AFTER TIMESTEP', 'air_density'),
              ('eastward_wind', 'x_wind'),
              ('northward_wind', 'y_wind')]

# Correct units for some cubes
units = [('air_density', 'kg m-3'),
         ('dimensionless_exner_function', '1'),
         ('mass_fraction_of_cloud_ice_in_air', '1'),
         ('mass_fraction_of_cloud_liquid_water_in_air', '1')]


def main():
    for infile, outfile in file_pairs:
        cubes = iris.load(infile)

        # Correct analysis oddities
        correct_analyses(cubes)

        # Calculate derived variables

        # Put the cubes in standard format on grid
        newcubes = files.redo_cubes(cubes, basis_cube, slices=slices)

        iris.save(newcubes, outfile)


def correct_analyses(cubes):
    for cube in cubes:
        # Give time coordinate proper name
        cube.coord('t').rename('time')

        # Correct dimensional coordinates
        cube.coord('Hybrid height').rename('level_height')
        cube.coord('grid_latitude').coord_system = lat.coord_system
        cube.coord('grid_longitude').coord_system = lon.coord_system

    # Correct cube names
    for before, after in name_pairs:
        cubes.extract(before)[0].rename(after)

    # Correct units
    for name, unit in units:
        cubes.extract(name)[0].units = unit

    # Convert density to true density
    rho = convert.calc('air_density', cubes)
    z = rho.coord('altitude')
    r = z.points + convert.r.data
    rho.data = rho.data / r ** 2

if __name__ == '__main__':
    main()
