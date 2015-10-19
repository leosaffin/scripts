import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
from mymodule import files, convert, grid, interpolate
from scripts import fronts


def main():
    filename = '/home/lsaffin/Documents/meteorology/programming/iop5_36h.pp'
    cubes = files.load(filename)
    cubes.remove(cubes.extract('air_pressure')[0])
    theta = convert.calc('air_potential_temperature', cubes)
    p = grid.make_coord(cubes.extract('air_pressure')[0])
    theta.add_aux_coord(p, [0, 1, 2])
    theta650 = interpolate.to_level(theta, air_pressure=[65000])
    loc = fronts.main(theta650.data[0])
    loc = theta650[0].copy(data=loc)
    qplt.contourf(theta650[0], np.linspace(280, 320, 31), cmap='gray',
                  extend='both')
    plt.gca().coastlines()
    plt.gca().gridlines()
    plt.title(r'$\theta$ at 650 hPa')
    iplt.contour(loc, [0], colors='b', linewidths=3)
    plt.savefig('../test_fronts5.png')


if __name__ == '__main__':
    loc = main()
