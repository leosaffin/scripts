import matplotlib.pyplot as plt
from mymodule import files, convert, plot


def main(cubes):
    """
    """
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('ertel_potential_vorticity', [2]))

    plot.pcolormesh(theta[0], cmap='plasma')
    plt.show()

if __name__ == '__main__':
    cubes = files.load('datadir/xjjhq/xjjhq_036.pp')
    main(cubes)
