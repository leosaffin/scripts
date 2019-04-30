"""Plot the number of grid boxes diagnosed to be modified by a physics scheme
as a function of precision.
"""

import parse
import matplotlib.pyplot as plt
import iris
from iris.analysis import SUM
from iris.exceptions import CoordinateCollapseError
from myscripts.statistics import count
from myscripts.models.speedy import datadir, sigma_levels, physics_schemes


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/'
    variable = 'Temperature'
    forecast_period = 2/3
    sigma = sigma_levels[0]

    # Load the cubes
    string = '{} Tendency due to'.format(variable)
    cs = iris.Constraint(cube_func=lambda x: string in x.name(),
                         sigma=sigma, forecast_period=forecast_period)
    cubes = iris.load(path + 'rp_*_tendencies.nc', cs)
    print(cubes)

    plot_active(cubes, string)
    plt.xlabel('Precision (sbits)')
    plt.ylabel('Number of gridpoints')
    plt.legend()
    plt.show()

    return


def plot_active(cubes, string):
    for cube in cubes:
        scheme, units = parse.parse(string + ' {} [{}]', cube.name())
        if scheme == 'Large-Scale Condensation':
            scheme = 'Condensation'

        plp = physics_schemes[scheme]

        nonzero = count(cube)
        try:
            nonzero = nonzero.collapsed('sigma', SUM)
        except CoordinateCollapseError:
            pass
        nonzero = nonzero/nonzero[-1]
        plp.plot(nonzero, label=scheme)
    return


if __name__ == '__main__':
    main()
