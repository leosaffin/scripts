import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import iris
import iris.plot as iplt
import iris.quickplot as qplt
from mymodule import files, convert, plot, interpolate, grid
from mymodule.plot import interactive


def main(cubes):
    """
    """
    diff = convert.calc('total_minus_advection_only_pv', cubes)
    theta = convert.calc('air_potential_temperature', cubes)
    pv = convert.calc('ertel_potential_vorticity', cubes)
    p = convert.calc('air_pressure', cubes)
    p = grid.make_coord(p)
    theta.add_aux_coord(p, [0, 1, 2])

    theta_p = interpolate.to_level(theta, air_pressure=[80000])
    theta.remove_coord('air_pressure')

    plotter1 = interactive.CrossSectionPlotter(diff, qplt.contourf,
                                               plot.even_cscale(2), cmap='bwr',
                                               extend='both')

    plotter2 = interactive.CrossSectionPlotter(theta, iplt.contour, [287],
                                               colors='r')
    plotter3 = interactive.CrossSectionPlotter(pv, plot.add_pv2)

    onselect = interactive.CrossSection([plotter1, plotter2, plotter3])

    qplt.contourf(theta_p[0], np.linspace(280, 320, 21), cmap='cubehelix_r')
    widget = RectangleSelector(plt.gca(), onselect, drawtype='line')

    plt.show()

if __name__ == '__main__':
    filename = '/home/lsaffin/Documents/meteorology/programming/iop5_36h.pp'
    cubes = files.load(filename,
                       iris.Constraint(model_level_number=lambda cell: cell <= 30))
    main(cubes)
