"""Calculate the forecast error relative to a reference forecast as a function
    of precision
"""
import parse
import iris
from myscripts.statistics import rms_diff
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/sppt_off/'
    name = 'Temperature [K]'
    pressure = 500

    filenames = {
        'Physics': 'rp_physics.nc',
        'Condensation': 'rp_condensation.nc',
        'Convection': 'rp_convection.nc',
        'Cloud': 'rp_cloud.nc',
        'Short-Wave Radiation': 'rp_sw_radiation.nc',
        'Long-Wave Radiation': 'rp_lw_radiation.nc',
        'Surface Fluxes': 'rp_surface_fluxes.nc',
        'Vertical Diffusion': 'rp_vertical_diffusion.nc',
    }

    # Load the reduced precision and reference forecasts
    cs = iris.Constraint(name=name, pressure=pressure)

    ref = iris.load_cube(path + 'rp_physics.nc', cs)
    ref = ref.extract(iris.Constraint(precision=52))
    print(ref)

    newcubes = iris.cube.CubeList()
    for scheme in filenames:
        cube = iris.load_cube(path + filenames[scheme], cs)
        print(cube)

        # Calculate the global (weighted) rms error as a function of precision
        diff = rms_diff(cube, ref)
        diff.rename(
            '{} with {} in reduced precision'.format(diff.name(), scheme))
        newcubes.append(diff)

    print(newcubes)
    name = name.split(' [')[0].lower().replace(' ', '_')
    filename = 'precision_errors_{}_{}hpa.nc'.format(name, pressure)
    iris.save(newcubes, datadir + filename)

    return


def decode_name(name):
    """Extract information from names created in main function

    The string will follow the format:

    `RMS error in {variable} [{units}] with {scheme} in reduced precision`

    Args:
        name (str): The variable name following the above format

    Returns
        variable (str): The variable name
        units (str): The variable units
        scheme (str): The scheme that is in reduced precision
    """
    variable, units, scheme = parse.parse(
        'RMS error in {} [{}] with {} in reduced precision', name)

    return variable, units, scheme


if __name__ == '__main__':
    main()
