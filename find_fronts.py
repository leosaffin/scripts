import matplotlib.pyplot as plt
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
    return loc


if __name__ == '__main__':
    loc = main()
    plt.contour(loc, [0])
    plt.savefig('../test_fronts.png')
