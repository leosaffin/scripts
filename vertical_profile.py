"""Calculate averaged vertical profiles of PV tracers
"""

import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.analysis import VARIANCE
from mymodule import files, convert
from mymodule.user_variables import datadir, plotdir
from myscripts.plot import linestyles, colors


def main():
    filename = datadir + 'xjjhq/xjjhqa_036.pp'
    names = ['total_minus_advection_only_pv',
             'long_wave_radiation_pv',
             'microphysics_pv',
             'convection_pv',
             'boundary_layer_pv',
             'advection_inconsistency_pv',
             'residual_pv']
    cubes = files.load(filename)
    variables = [convert.calc(name, cubes) for name in names]
    means = [x.collapsed(['grid_latitude', 'grid_longitude'], VARIANCE)
             for x in variables]
    plotfig(means)


def plotfig(means):
    for n, mean in enumerate(means):
        iplt.plot(mean, mean.coord('level_height'), linestyle=linestyles[n],
                  color=colors[n], label=mean.name().replace('_', ' '))
    plt.axis([0, 1, 0, 18000])
    plt.axvline(color='k')
    plt.savefig(plotdir + '36h_vertical_profile.png')
    plt.legend(loc='best')
    plt.savefig(plotdir + '36h_vertical_profile_legend.png')


if __name__ == '__main__':
    main()
