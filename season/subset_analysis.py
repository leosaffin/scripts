"""Replaces an analysis with a .pp file with a subset of cubes
"""

import glob
import iris
from mymodule import files, convert


# List of variables to extract from the analysis
names = ['advection_only_pv', # Equal to PV
         'advection_only_potential_temperature', # Equal to theta
         'total_pv', # Calculate PV
         'short_wave_radiation_pv', # Set to zero
         'long_wave_radiation_pv', # Set to zero
         'microphysics_pv', # Set to zero
         'gravity_wave_drag_pv', # Set to zero
         'convection_pv', # Set to zero
         'boundary_layer_pv', # Set to zero
         'advection_inconsistency_pv', # Set to zero
         'cloud_rebalancing_pv', # Set to zero
         'air_pressure_at_sea_level', # Calculate from prognostic variables
         'atmosphere_boundary_layer_thickness',
         'stratiform_rainfall_amount', # Set to zero
         'convective_rainfall_amount', # Set to zero
         'x_wind',
         'y_wind',
         'upward_air_velocity',
         'air_pressure', # Calculate from exner pressure
         'surface_pressure', # Calculate from exner pressure
         'specific_humidity',
         'mass_fraction_of_cloud_liquid_water_in_air',
         'mass_fraction_of_cloud_ice_in_air',
         'air_temperature', # Calculate from theta and exner pressure
         'surface_altitude']


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
        cube = convert.calc(name, cubelist)[0]
        # Remove coordinates that make save/load not work
        try:
            cube.remove_aux_factory(cube.aux_factory('altitude'))
            cube.remove_coord('surface_altitude')
            if name == 'y_wind':
                cube = cube[0:50, 14:344, 15:585]
            else:
                cube = cube[0:50, 15:345, 15:585]
        except iris.exceptions.CoordinateNotFoundError:
            cube = convert.calc(name, cubelist)[0]
            cube = cube[15:345, 15:585]
        newcubelist.append(cube)
    iris.save(newcubelist, output_file)


if __name__ == '__main__':
    main()
