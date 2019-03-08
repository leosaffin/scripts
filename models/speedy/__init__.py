from myscripts import datadir, plotdir
from myscripts.plots.colourblind import *
from irise.plot.util import PlotParameter

datadir = datadir + 'speedy/'
plotdir = plotdir + 'speedy/'

sigma_levels = [0.95, 0.835, 0.685, 0.51, 0.34, 0.2, 0.095, 0.025]
pressure_levels = [925, 850, 700, 500, 300, 200, 100, 30]

physics_schemes = {
    'All Parametrizations': PlotParameter(color='k',    linestyle='--', idx=0),
    'Physics':              PlotParameter(color='k',    linestyle='-',  idx=0),
    'Convection':           PlotParameter(color=blue,   linestyle='-',  idx=1),
    'Condensation':         PlotParameter(color=purple, linestyle='--', idx=2),
    'Cloud':                PlotParameter(color=brown,  linestyle='-',  idx=3),
    'Short-Wave Radiation': PlotParameter(color=orange, linestyle='-',  idx=4),
    'Long-Wave Radiation':  PlotParameter(color=red,    linestyle='--', idx=5),
    'Surface Fluxes':       PlotParameter(color=green,  linestyle='-',  idx=6),
    'Vertical Diffusion':   PlotParameter(color=pink,   linestyle='--', idx=7),
    'SPPT':                 PlotParameter(color='k',    linestyle='--', idx=8),
}
