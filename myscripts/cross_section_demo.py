import matplotlib
import matplotlib.pyplot as plt

import iris.quickplot as qplt

from irise.plot.interactive import CrossSection as CS
from irise.plot.interactive import CrossSectionPlotter as CSP

# Importing iris.tests overrides the matplotlib backend
backend = matplotlib.get_backend()
from iris.tests import stock
matplotlib.use(backend)


def main():
    """
    """
    cube = stock.realistic_4d()

    plotter = CSP(True, qplt.pcolormesh, cube[0])

    qplt.pcolormesh(cube[0, 0])
    ax = plt.gca()
    ax.coastlines()
    ax.gridlines()

    cross_section = CS(plt.gcf(), ax, plotters=[plotter])

    plt.show()


if __name__ == '__main__':
    main()
