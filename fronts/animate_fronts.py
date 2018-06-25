import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from mymodule import files, convert
from mymodule.user_variables import datadir, plotdir


def main():
    """
    """
    cs = iris.Constraint(pressure=900)
    for i in xrange(1, 37):
        # Load the front variables
        cubes = files.load(datadir + '/xjjhq/xjjhq_fronts' +
                           str(i).zfill(3) + '.pp')
        loc = convert.calc('front_locator_parameter_thw', cubes)
        m1 = convert.calc('thermal_front_parameter_thw', cubes)
        m2 = convert.calc('local_frontal_gradient_thw', cubes)

        # Apply the masking criteria
        mask = np.logical_or(m1.data < 4 * 0.3e-10, m2.data < 4 * 1.35e-5)
        loc.data = np.ma.masked_where(mask, loc.data)
        loc = cs.extract(loc)

        # Plot the locating variable
        qplt.contour(loc, [0], colors='k')
        plt.gca().coastlines()
        plt.gca().gridlines()
        plt.title('Fronts at 900 hPa, T+' + str(i) + ' hours')
        plt.savefig(plotdir + 'fronts' + str(i).zfill(3) + '.png')


if __name__ == '__main__':
    main()
