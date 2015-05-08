"""Replaces an analysis with a .pp file with a subset of cubes
"""

import glob
import iris


# List of variables to extract from the analysis
names = ['x_wind', 'y_wind', 'upward_air_velocity',
         'air_potential_temperature', 'dimensionless_exner_function',
         'specific_humidity', 'mass_fraction_of_cloud_ice_in_air',
         'mass_fraction_of_cloud_liquid_water_in_air',
         'atmosphere_boundary_layer_thickness', 'surface_altitude']


def main():
    """ Modifies all .analysis files in the current directory
    """
    for analysis_file in glob.glob('*.analysis.pp'):
        output_file = analysis_file + '.pp'
        newpp(analysis_file, output_file)


def newpp(analysis_file, output_file):
    """ Copies an analysis file taking a subset of variables
    """
    cubelist = iris.load(analysis_file)
    newcubelist = iris.cube.CubeList()
    for name in names:
        cube = cubelist.extract(name)[0]
        # Remove coordinates that make save/load not work
        try:
            cube.remove_aux_factory(cube.aux_factory('altitude'))
            cube.remove_coord('surface_altitude')
            cube = cube[0:50, 15:345, 15:585]
        except iris.exceptions.CoordinateNotFoundError:
            cube = cubelist.extract(name)[0]
            cube = cube[15:345, 15:585]
        newcubelist.append(cube)
    newcubelist = nddiag(newcubelist)
    iris.save(newcubelist, output_file)


def nddiag(cubelist):
    """ Replace prognostic variables with NDdiag fields
    """
    return cubelist

if __name__ == '__main__':
    main()
