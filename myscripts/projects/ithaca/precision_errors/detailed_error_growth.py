import math

import numpy as np
import matplotlib.pyplot as plt

import iris
import iris.plot as iplt

from irise import plot
from myscripts.statistics import rms_diff
from myscripts.models.speedy import datadir, plotdir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/sppt_off/'
    variable = 'Temperature'
    level = 500.

    filename = 'rp_physics.nc'
    cs = iris.Constraint(name=variable, pressure=level, precision=52)
    cube_fp = iris.load_cube(path + filename, cs)

    cs = iris.Constraint(name=variable, pressure=level, precision=51)
    cube_rp = iris.load_cube(path + filename, cs)

    diff = cube_rp - cube_fp
    rmse = rms_diff(cube_rp, cube_fp)
    t = rmse.coord('forecast_period').points

    limit = 0.
    for n in range(rmse.shape[0]):
        # Create a one by two grid with shared x and y axes along rows and columns
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[16, 5])

        plt.axes(axes[0])
        iplt.plot(rmse)
        plt.plot(t[n], rmse.data[n], 'kx')

        plt.axes(axes[1])
        new_limit = np.abs(diff[n].data).max()
        print(new_limit)
        if new_limit > 0:
            # Round to one decimal place but always up
            order_of_magnitude = 10 ** math.floor(np.log10(new_limit))
            print(order_of_magnitude)
            new_limit = math.ceil(new_limit/order_of_magnitude) * order_of_magnitude

        limit = max(limit, new_limit)
        print(limit)
        plot.pcolormesh(diff[n], vmin=-limit, vmax=limit, cmap='coolwarm')

        plt.savefig(plotdir + 'detailed_error_growth_51_52_' + str(n).zfill(4) + '.png')

        plt.close()

    return


if __name__ == '__main__':
    main()
