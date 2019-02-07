"""
Plot the overlapping coefficient between ensemble forecasts
"""

import matplotlib.pyplot as plt
import iris
from irise.plot.util import legend
from myscripts.models.speedy import datadir, physics_schemes


def main():
    path = datadir + 'stochastic/ensembles/'

    files = [
        ('overlap_52_52.nc', 'Physics (52 sbit)', '-', 'purple'),
        ('overlap_52_23.nc', 'Physics (23 sbit)', '-', 'k'),
        ('overlap_52_10.nc', 'Physics (10 sbit)', '--', 'k'),
        ('overlap_52_8.nc', 'Physics (8 sbit)', ':', 'k'),
        ('overlap_52_cnv8.nc', 'Convection (8 sbit)', '--', 'b'),
        ('overlap_52_sflx8.nc', 'Surface Fluxes (8 sbit)', '--', 'grey'),
        ('overlap_52_vdif8.nc', 'Vertical Diffusion (8 sbit)', '-', 'g')
        ]

    for filename, label, linestyle, color in files:
        overlap = iris.load_cube(path + filename)

        plp = physics_schemes[label.split(' (')[0]]
        plp.plot(overlap, label=label, linestyle=linestyle, color=color)

    legend()
    plt.show()
    return


if __name__ == '__main__':
    main()
