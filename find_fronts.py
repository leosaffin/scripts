import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
from mymodule import files, convert, grid, interpolate
from mymodule.detection.fronts import fronts


def main(p_level):
    filename = '/home/lsaffin/Documents/meteorology/programming/iop5_36h.pp'
    cubes = files.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    theta = convert.calc('air_potential_temperature', cubes)
    p = grid.make_coord(cubes.extract('air_pressure')[0])
    theta.add_aux_coord(p, [0, 1, 2])
    theta_p = interpolate.to_level(theta, air_pressure=[p_level])
    loc = fronts.main(theta_p.data[0])
    loc = theta_p[0].copy(data=loc)
    qplt.contourf(theta_p[0], np.linspace(280, 320, 41), cmap='gray',
                  extend='both')
    plt.gca().coastlines()
    plt.gca().gridlines()
    plt.title(r'$\theta$ at 650 hPa')
    iplt.contour(loc, [0], colors='b', linewidths=3)
    plt.savefig('../test_fronts5.png')


if __name__ == '__main__':
    p_level = 85000
    main(p_level)
