"""Produce a multi-panel figure of each output lead time in a forecast
"""

import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from mymodule.user_variables import plotdir
from myscripts import case_studies


columns = 3


def main(forecast, name, levels, *args,  **kwargs):
    nt = len(forecast)
    rows = (nt / columns) + 1
    fig = plt.figure(figsize=(18, 10 * float(rows) / columns))
    for n, cubes in enumerate(forecast):
        row = n / columns
        column = n - row * columns
        print(row, column)
        ax = plt.subplot2grid((rows, columns), (row, column))

        cube = convert.calc(name, cubes, levels=levels)[0]
        im = iplt.pcolormesh(cube, *args, **kwargs)
        plot._add_map()

    ax = plt.subplot2grid((rows, columns), (row, column + 1))
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')
    plt.savefig(plotdir + name + '_' + str(levels[0]) +
                '_' + str(levels[1][0]) + '.png')

    return


if __name__ == '__main__':
    forecast = case_studies.generate_season_forecast(2013, 11, 1)
    name = 'ertel_potential_vorticity'
    levels = ('air_potential_temperature', [320])
    main(forecast, name, levels, vmin=0, vmax=10, cmap='cubehelix_r')
