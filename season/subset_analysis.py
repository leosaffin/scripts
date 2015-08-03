"""Replaces an analysis with a .pp file with a subset of cubes
"""

import glob
import iris
from mymodule import files, convert


# List of variables to extract from the analysis
names = ['advection_only_pv', # ?
         'advection_only_potential_temperature', # ?
         'total_pv', # ?
         'short_wave_radiation_pv', # ?
         'long_wave_radiation_pv', # ?
         'microphysics_pv', # ?
         'gravity_wave_drag_pv', # ?
         'convection_pv', # ?
         'boundary_layer_pv', # ?
         'advection_inconsistency_pv', # ?
         'cloud_rebalancing_pv', # ?
         'air_pressure_at_sea_level', # ?
         'atmosphere_boundary_layer_thickness',
         'stratiform_rainfall_amount', # ?
         'convective_rainfall_amount', # ?
         'x_wind',
         'y_wind',
         'upward_air_velocity',
         'air_pressure', # ?
         'surface_pressure', # ?
         'specific_humidity',
         'mass_fraction_of_cloud_liquid_water_in_air',
         'mass_fraction_of_cloud_ice_in_air',
         'air_temperature', # ?
         'surface_altitude']


def main():
    """ Modifies all .analysis files in the current directory
    """
    for analysis_file in glob.glob('*.analysis.pp'):
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
