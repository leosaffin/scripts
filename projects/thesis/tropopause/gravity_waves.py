import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import iris.quickplot as qplt
import iris.plot as iplt
from mymodule import convert, plot, calculus
from mymodule.plot.util import even_cscale
from mymodule.plot.interactive import CrossSection as CS
from mymodule.plot.interactive import CrossSectionPlotter as CSP
from myscripts.models.um import case_studies

names = ['gravity_wave_drag_pv', 'convection_pv', 'boundary_layer_pv',
         'dynamics_tracer_inconsistency']


def main(cubes):
    # Set up cross section plotters
    pv = convert.calc('ertel_potential_vorticity', cubes)
    adv = convert.calc('advection_only_pv', cubes)
    T = convert.calc('air_temperature', cubes)
    dtdz = calculus.multidim(T, 'altitude', 'z')
    for cube in [pv, adv, dtdz]:
        cube.coord('altitude').convert_units('km')
        cube.coord('atmosphere_hybrid_height_coordinate').convert_units('km')
        cube.coord('surface_altitude').convert_units('km')
    plotters = []
    for name in names:
        cube = convert.calc(name, cubes)
        cube.coord('altitude').convert_units('km')
        cube.coord('atmosphere_hybrid_height_coordinate').convert_units('km')
        cube.coord('surface_altitude').convert_units('km')
        plotter1 = CSP(True, qplt.contourf, cube, even_cscale(5),
                       cmap='coolwarm', extend='both')
        plotter2 = CSP(False, iplt.contour, pv, [2], colors='k')
        plotter3 = CSP(False, iplt.contour, adv, [2], colors='k',
                       linestyles='--')
        plotter4 = CSP(False, iplt.contour, dtdz, [-0.002], colors='k',
                       linestyles=':')
        plotters.append(plotter1)
        plotters.append(plotter2)
        plotters.append(plotter3)
        plotters.append(plotter4)

    onselect = CS(plotters)

    # Plot theta on 2-PVU to identify regions
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('ertel_potential_vorticity', [2]))[0]
    theta.data = np.ma.masked_where(theta.data > 340, theta.data)
    plot.contourf(theta, np.linspace(280, 340, 13))

    # Create Cross-sections
    selector = RectangleSelector(plt.gca(), onselect, drawtype='line')
    plt.show()

    return


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=36)
    main(cubes)
