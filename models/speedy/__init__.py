from mymodule.user_variables import datadir, plotdir
from mymodule.plot.util import PlotParameter

datadir = datadir + 'speedy/'
plotdir = plotdir + 'speedy/'

physics_schemes = {
    'Physics':              PlotParameter(color='k',    linestyle='-',  idx=0),
    'Convection':           PlotParameter(color='b',    linestyle='--', idx=1),
    'Condensation':         PlotParameter(color='b',    linestyle='-',  idx=2),
    'Cloud':                PlotParameter(color='grey', linestyle='-',  idx=3),
    'Short-Wave Radiation': PlotParameter(color='r',    linestyle=':',  idx=4),
    'Long-Wave Radiation':  PlotParameter(color='r',    linestyle='--', idx=5),
    'Surface Fluxes':       PlotParameter(color='grey', linestyle='--', idx=6),
    'Vertical Diffusion':   PlotParameter(color='g',    linestyle='-',  idx=7),
    'SPPT':                 PlotParameter(color='k',    linestyle='--', idx=8),
}
