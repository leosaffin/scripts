"""
Start by running the script conv2nc.tcl on the raw analyses from the xcm
"""

import datetime
import iris
from iris.cube import CubeList
from iris.util import squeeze
from mymodule import constants, grid
import files

# Define which area of grid to subset
slices = slice(0, 50), slice(15, 345), slice(15, 585)

# Load basis cube
basis_cube = iris.load_cube('/projects/diamet/lsaffi/temp/prognostics_001.nc',
                            'air_potential_temperature')
lat = grid.extract_dim_coord(basis_cube, 'y')
lon = grid.extract_dim_coord(basis_cube, 'x')

basis_raw_cubes = iris.load('/projects/diamet/lsaffi/temp/xliba.analysis')

# Define how to rename variables
name_pairs = [('DENSITY*R*R AFTER TIMESTEP', 'air_density'),
              ('eastward_wind', 'x_wind'),
              ('northward_wind', 'y_wind')]

# Correct units for some cubes
units = [('air_density', 'kg m-3'),
         ('dimensionless_exner_function', '1'),
         ('mass_fraction_of_cloud_ice_in_air', '1'),
         ('mass_fraction_of_cloud_liquid_water_in_air', '1')]


def main(file_pairs, time):
    for infile, outfile in file_pairs:
        print(infile, outfile)
        cubes = iris.load(infile)

        # Extract and remove surface altitude
        z_0 = cubes.extract('surface_altitude', [0])
        cubes.remove(z_0)
        z_0 = grid.make_coord(squeeze(z_0))

        # Correct analysis oddities
        cubes = correct_analyses(cubes)

        # Add hybrid height coordinates to variables
        for name in ('x_wind', 'y_wind', 'upward_air_velocity',
                     'air_potential_temperature'):
            cube = cubes.extract(name)[0]
            cube_0 = basis_raw_cubes.extract(name)[0]
            sigma = cube_0.coord('sigma')
            z_surf = cube_0.coord('surface_altitude')
            add_hybrid_height(cube, sigma, z_surf)

        # Use field on rho levels for density
        rho = cubes.extract('air_density')[0]
        cube_0 = basis_raw_cubes.extract('x_wind')[0]
        sigma = cube_0.coord('sigma')
        add_hybrid_height(rho, sigma, z_0)

        # Convert density to true density
        z_rho = rho.coord('altitude')
        r = z_rho.points + constants.r.data
        rho.data = rho.data / r ** 2

        # Remove the bottom level from w
        w = cubes.extract('upward_air_velocity')[0]
        cubes.remove(w)
        w = w[1:]
        cubes.append(w)

        # Calculate derived variables
        files.derived(cubes)

        # Put the cubes in standard format on grid
        newcubes = files.redo_cubes(
            cubes, basis_cube, slices=slices, time=time)

        iris.save(newcubes, outfile)


def correct_analyses(cubes):
    newcubes = CubeList()

    for cube in cubes:
        # Squeeze cubes dimensions
        newcube = squeeze(cube)

        # Give time coordinate proper name
        newcube.coord('t').rename('time')

        # Correct dimensional coordinates
        newcube.coord('Hybrid height').units = 'm'
        newcube.coord('Hybrid height').attributes = {'positive': 'up'}
        newcube.coord('Hybrid height').rename('level_height')
        newcube.coord('grid_latitude').coord_system = lat.coord_system
        newcube.coord('grid_longitude').coord_system = lon.coord_system

        newcubes.append(newcube)

    # Correct cube names
    for before, after in name_pairs:
        newcubes.extract(before)[0].rename(after)

    # Correct units
    for name, unit in units:
        newcubes.extract(name)[0].units = unit

    return newcubes


def add_hybrid_height(cube, sigma, z_0):
    cube.add_aux_coord(sigma, [0])
    cube.add_aux_coord(z_0, [1, 2])

    grid.add_hybrid_height(cube)


def generate_file_pairs(t_0, dt, nt, path):
    """

    Args:
        t_0 (datetime.datetime): Time of first analysis file

        dt (datetime.timedelta): Time spacing between analysis files

        nt (int): Number of analysis files

        path (str): Directory containing analysis files

    Returns:
        file_pairs (list): List of tuples containing infile and outfile
    """
    file_pairs = []
    for n in range(nt):
        time = t_0 + n * dt
        YYYYMMDD, HH = time2str(time)
        file_pairs.append((path + YYYYMMDD + '_qwqy' + HH + '.nc',
                           path + YYYYMMDD + '_analysis' + HH + '.nc'))
    return file_pairs


def time2str(t):
    """Extract two string of YYYYMMDD and HH from a datetime object

    Args:
        t (datetime.datetime)
    """
    YYYYMMDD = str(t)[0:10].replace('-', '')
    HH = str(t)[11:13]
    return YYYYMMDD, HH

if __name__ == '__main__':
    # IOP5
    t_0 = datetime.datetime(2011, 11, 28, 12)
    dt = datetime.timedelta(hours=6)
    nt = 7
    path = '/projects/diamet/lsaffi/iop5/'
    file_pairs = generate_file_pairs(t_0, dt, nt, path)
    time = 'hours since 2011-11-28 12:00:00'
    main(file_pairs, time)

    # IOP8
    t_0 = datetime.datetime(2011, 12, 7, 12)
    dt = datetime.timedelta(hours=6)
    nt = 7
    path = '/projects/diamet/lsaffi/iop8/'
    file_pairs = generate_file_pairs(t_0, dt, nt, path)
    time = 'hours since 2011-12-07 12:00:00'
    main(file_pairs, time)

    # Systematic Forecasts
    t_0 = datetime.datetime(2013, 11, 1)
    dt = datetime.timedelta(days=1)
    nt = 92
    path = '/projects/diamet/lsaffi/season/'
    file_pairs = generate_file_pairs(t_0, dt, nt, path)
    time = 'hours since 2013-11-01 00:00:00'
    main(file_pairs, time)
