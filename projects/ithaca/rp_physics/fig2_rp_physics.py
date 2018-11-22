"""
Similar to the first plot but with lines for individual physics schemes in
reduced precision. Show error vs time for one precision and error vs precision
for one time. Repeat for SPPT off and on.
"""

import matplotlib.pyplot as plt
import iris
from mymodule.plot.util import legend, multilabel
from myscripts.models.speedy import datadir, physics_schemes
from myscripts.projects.ithaca.precision_errors import decode_name


def main():
    # Specify which files and variable to compare
    path = datadir + 'output/'
    factor = 0.01
    variable = 'temperature'

    time_cs = iris.Constraint(forecast_period=14)
    precision_cs = iris.Constraint(precision=10)

    # Create a two by two grid with shared x and y axes along rows and columns
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex='col', sharey=True)

    # Deterministic
    filename = 'precision_errors_{}_500hpa.nc'.format(variable)
    make_plot_pair(path + filename, time_cs, precision_cs, axes, 0, factor)

    # Stochastic
    filename = 'precision_errors_{}_500hpa_stochastic.nc'.format(variable)
    make_plot_pair(path + filename, time_cs, precision_cs, axes, 1, factor)

    plt.xlim(5, 23)
    plt.ylim(0, 4)
    plt.show()

    return


def make_plot_pair(filename, time_cs, precision_cs, axes, n, factor):
    cubes = iris.load(filename)
    for cube in cubes:
        cube.coord('forecast_period').convert_units('days')

    plt.axes(axes[n, 0])
    multilabel(axes[n, 0], 2*n, factor=factor)
    make_plot(cubes, precision_cs)

    if n == 0:
        legend(key=lambda x: physics_schemes[x[0]].idx, ncol=2,
               title='Physics Schemes')
    elif n == 1:
        plt.xlabel('Forecast Lead Time [days]')

    plt.axes(axes[n, 1])
    multilabel(axes[n, 1], 2*n + 1, factor=factor)
    make_plot(cubes, time_cs)

    if n == 1:
        plt.xlabel('Precision [sbits]')
    return


def make_plot(cubes, cs):
    subcubes = cubes.extract(cs)
    for cube in subcubes:
        variable, scheme = decode_name(cube.name())
        plp = physics_schemes[scheme]
        plp.plot(cube, label=scheme)
    return


if __name__ == '__main__':
    main()
