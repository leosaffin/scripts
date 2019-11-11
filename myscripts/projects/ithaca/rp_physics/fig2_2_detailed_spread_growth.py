"""Plot the ensemble spread of the double-precision ensemble at various lead
times
"""

import matplotlib.pyplot as plt

import iris
from iris.analysis import STD_DEV

from irise import plot
from myscripts.plot import get_row_and_column_index, get_cscale_limit
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'stochastic/ensembles/'
    variable = 'Temperature'
    level = 500.
    days = [2, 4, 10, 20]

    filename = 'rp_physics_52b.nc'
    cs = iris.Constraint(name=variable, pressure=level)
    cube_fp = iris.load_cube(path + filename, cs)

    spread = cube_fp.collapsed('ensemble_member', STD_DEV)

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=[16, 10])

    limit = 0.
    for n in days:
        row, col = get_row_and_column_index(n, ncols=2)
        plt.axes(axes[row, col])

        limit = get_cscale_limit(spread[n].data, limit)
        plot.pcolormesh(spread[n], vmin=0, vmax=limit, cmap='cubehelix_r')
        plt.title(str(n) + ' days')

    plt.show()

    return


if __name__ == '__main__':
    main()
