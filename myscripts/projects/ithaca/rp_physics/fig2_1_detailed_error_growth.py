"""Plot the difference with respect to double precision of a reduced precision
deterministic run

These differences have a strange error growth. Plot the four stages:

    1) Random errors in the small-scale spectral modes
    2) Flip one gridpoint in convection scheme and errors grows from there
    3) Random differences in convection. Dominated by error in the tropics
    4) Baroclinic error growth - extratropics start to dominate errors
"""

import matplotlib.pyplot as plt

import iris

from irise import plot
from myscripts.plot import get_row_and_column_index, get_cscale_limit
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/sppt_off/'
    variable = 'Temperature'
    level = 500.
    days = [2, 4, 10, 20]

    # Load the double precision and reduced precision model runs
    filename = 'rp_physics.nc'
    cs = iris.Constraint(name=variable, pressure=level, precision=52)
    cube_fp = iris.load_cube(path + filename, cs)

    cs = iris.Constraint(name=variable, pressure=level, precision=23)
    cube_rp = iris.load_cube(path + filename, cs)

    diff = cube_rp - cube_fp

    # 2x2 figure. 1 plot for each stage of error growth
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=[16, 10])

    limit = 0.
    for n in days:
        row, col = get_row_and_column_index(days.index(n), ncols=2)
        plt.axes(axes[row, col])

        limit = get_cscale_limit(diff[n].data, limit)
        plot.pcolormesh(diff[n], vmin=-limit, vmax=limit, cmap='coolwarm')
        plt.title(str(n) + ' days')

    plt.show()

    return


if __name__ == '__main__':
    main()
