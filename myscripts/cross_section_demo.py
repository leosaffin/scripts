import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import iris.quickplot as qplt
from irise import files, convert
from irise.plot.interactive import CrossSection as CS
from irise.plot.interactive import CrossSectionPlotter as CSP
from myscripts import datadir


def main():
    """
    """
    filename = datadir + 'iop5_36h.pp'
    cubes = files.load(filename)

    theta = convert.calc('air_potential_temperature', cubes)

    plotter = CSP(False, qplt.contourf, theta, np.linspace(270, 350, 15),
                  cmap='cubehelix_r', extend='both')

    onselect = CS([plotter])

    qplt.contourf(theta[0], np.linspace(270, 300, 31), cmap='cubehelix_r')
    RectangleSelector(plt.gca(), onselect, drawtype='line')

    plt.show()


if __name__ == '__main__':
    main()
