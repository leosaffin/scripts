import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
from mymodule import files, convert, grid, interpolate
from mymodule.detection.fronts import fronts


def main(p_level):
    # Load data
    filename = '/home/lsaffin/Documents/meteorology/programming/iop5_36h.pp'
    cubes = files.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    theta = convert.calc('air_potential_temperature', cubes)

    # Interpolate to pressure level
    p = grid.make_coord(cubes.extract('air_pressure')[0])
    theta.add_aux_coord(p, [0, 1, 2])
    theta_p = interpolate.to_level(theta, air_pressure=[p_level])[0]

    # Calculate the fronts
    loc = fronts.main(theta_p)
    loc = theta_p.copy(data=loc)

    # Plot the output
    qplt.contourf(theta_p, np.linspace(280, 320, 41),
                  cmap='gray', extend='both')
    plt.gca().coastlines()
    plt.gca().gridlines()
    plt.title(r'$\theta$ at ' + str(p_level) + ' Pa')
    iplt.contour(loc, [0], colors='b', linewidths=3)
    plt.savefig('../test_fronts.png')


if __name__ == '__main__':
    p_level = 65000
    main(p_level)
