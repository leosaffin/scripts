"""
Plot the overlapping coefficient between ensemble forecasts
"""

import matplotlib.pyplot as plt
import iris
import iris.coords
import iris.plot as iplt
from iris.analysis import MIN, MAX, MEAN
from irise.plot.util import legend, multilabel

from myscripts.models.speedy import datadir, physics_schemes


def main():
    path = datadir + 'stochastic/ensembles/'

    # Get overlap from exchanged ensembles
    ovl_range = iris.load(path + 'ovl_perturbed_??.nc')

    for n, cube in enumerate(ovl_range):
        cube.add_aux_coord(iris.coords.AuxCoord(n, long_name='ensemble'))

    ovl_range = ovl_range.merge_cube()
    ovl_range.coord('forecast_period').convert_units('days')

    ovl_min = ovl_range.collapsed('ensemble', MIN)
    ovl_max = ovl_range.collapsed('ensemble', MAX)
    ovl_mean = ovl_range.collapsed('ensemble', MEAN)

    # Two panels
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=[16, 5])

    # Panel 1 -
    plt.axes(axes[0])
    multilabel(axes[0], 0, 0.01)
    plt.fill_between(ovl_range.coord('forecast_period').points,
                     ovl_min.data, ovl_max.data, color='grey')

    files = [
        ('overlap_52_23.nc', '23 sbit', '-', 'k'),
        ('overlap_52_10.nc', '10 sbit', '--', 'k'),
        ('overlap_52_8.nc', '8 sbit', ':', 'k'),
        ('overlap_52_adj8.nc', '8 sbit, Fixed', '--', 'y'),
        ('overlap_52_half_precision_exponent.nc', '10 sbit, Exponent', '-', 'y')
        ]

    for filename, label, linestyle, color in files:
        overlap = iris.load_cube(path + filename)
        overlap.coord('forecast_period').convert_units('days')
        iplt.plot(overlap, label=label, color=color, linestyle=linestyle)

    legend()

    # Panel 2
    plt.axes(axes[1])
    multilabel(axes[1], 1, 0.01)
    plt.fill_between(ovl_range.coord('forecast_period').points,
                     ovl_min.data, ovl_max.data, color='grey')

    files = [
        ('overlap_52_cnv8.nc', 'Convection'),
        ('overlap_52_cond8.nc', 'Condensation'),
        ('overlap_52_swrad8.nc', 'Short-Wave Radiation'),
        ('overlap_52_lwrad8.nc', 'Long-Wave Radiation'),
        ('overlap_52_sflx8.nc', 'Surface Fluxes'),
        ('overlap_52_vdif8.nc', 'Vertical Diffusion'),
        ]

    for filename, label in files:
        overlap = iris.load_cube(path + filename)
        overlap.coord('forecast_period').convert_units('days')

        plp = physics_schemes[label]
        plp.plot(overlap, label=label)

    legend()
    plt.ylabel('Overlapping Coefficient')
    fig.text(0.5, 0.01, 'Forecast Lead Time [days]', ha='center')

    plt.show()
    return


if __name__ == '__main__':
    main()
