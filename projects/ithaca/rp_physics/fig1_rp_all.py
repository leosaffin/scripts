"""
Show the forecasts errors from experiments with all physics schemes in reduced
precision. Want to show error vs time for a range of precisions as well as error
vs precision for a range of times. Repeat with logarithmic scaling to better
see similarities and differences.
"""

import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from mymodule.plot.util import multilabel
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'output/'
    filename = 'precision_errors_geopotential_height_500hpa.nc'
    factor = 0.01

    # Set colour, linestyle and marker for each individual line
    cm = plt.cm.tab10
    # Plots vs precision
    precisions = [(10, cm(0.0), '-', '',),
                  (23, cm(0.1), '-', '',),
                  (51, cm(0.2), '-', '',),
                  (14, cm(0.3), '--', '',),
                  (15, cm(0.4), '--', '',),
                  (16, cm(0.5), '--', '',),
                  (35, cm(0.6), ':', '',),
                  (40, cm(0.7), ':', '',),
                  (45, cm(0.8), ':', '',),
                  ]

    # Plots vs lead time
    lead_times = [(1, cm(0.0), '-', ''),
                  (2, cm(0.1), '--', ''),
                  (3, cm(0.2), ':', ''),
                  (7, cm(0.3), '-', ''),
                  (14, cm(0.4), '--', ''),
                  (28, cm(0.5), ':', '')]

    # Load the cube with the rms errors
    cs = iris.Constraint(
        name='RMS error in Geopotential Height with Physics in reduced precision')
    cube = iris.load_cube(path + filename, cs)
    cube.coord('forecast_period').convert_units('days')

    # Create a two by two grid with shared x and y axes along rows and columns
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex='col', sharey='row',
                             figsize=[9.6, 7.2])

    # Normal yscale and log scale
    for n in range(2):
        # Error vs time
        plt.axes(axes[n, 0])
        multilabel(axes[n, 0], 2*n, factor=factor)
        make_plot(cube, precisions, 'precision')

        if n == 0:
            plt.legend(title='Precision [sbits]', ncol=3)
        elif n == 1:
            plt.xlabel('Forecast Lead Time [days]')


        # Error vs precision
        plt.axes(axes[n, 1])
        multilabel(axes[n, 1], 2*n + 1, factor=factor)
        make_plot(cube, lead_times, 'forecast_period')
        if n == 0:
            plt.legend(title='Lead Time [days]', ncol=2)
        elif n == 1:
            plt.xlabel('Precision [sbits]')

            # Put the second row of plots on a log scale
            plt.yscale('log')

    fig.text(0.05, 0.5, 'RMS Error in Geopotential Height [m]',
             va='center', rotation='vertical')
    plt.show()

    return


def make_plot(cube, parameters, label):
    for x, color, linestyle, marker in parameters:
        subcube = cube.extract(iris.Constraint(**{label: x}))
        iplt.plot(
            subcube, color=color, linestyle=linestyle, marker=marker, label=x)

    return


if __name__ == '__main__':
    main()
