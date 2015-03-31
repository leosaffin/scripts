'''
Name: Advection Inconsistency Paper

Creates all the plots required for the advection inconsistency paper
'''
import iris
import numpy as np
import matplotlib.pyplot as plt

from mymodule import load
from mymodule import convert
from mymodule import plot

def paper_plots(filename,diagnostics,model_level,levels):
    # Load cubes
    cubelist = load.full(filename)
    cubelist = cubelist.extract(iris.Constraint(model_level_number = 
                                                model_level))
    if suffix == '_5m':
        for n in xrange(len(cubelist)):
            cubelist[n] = cubelist[n][1]

    # Extract PV for plotting tropopause
    pv = convert.calc_tracer(cubelist,'advection_only_pv')

    for diag in diagnostics:
        # Extract relevant data
        cube = convert.calc_tracer(cubelist,diag)
        # Plot
        plot.level(cube,pv,levels,cmap='bwr',extend='both')
        # Save
        plt.savefig('/home/lsaffi/plots/paper/' + diag + suffix + '.png')
        plt.clf()

if __name__ == '__main__':
    diagnostics = ['missing_term','sum_of_physics_pv_tracers',
                   'advection_inconsistency_pv','residual_error']
    datadir = '/projects/diamet/lsaffi/'
    model_level = 33
    
    filename = datadir + 'xjjhn/xjjhna_pa0000'
    suffix = '_5m'
    levels = np.arange(-0.11,0.111,0.02)
    paper_plots(filename,diagnostics,model_level,levels)

    filename = datadir + 'xjjhq/xjjhqa_pa030'
    suffix = '_36h'
    levels = np.arange(-2.2,2.21,0.4)
    paper_plots(filename,diagnostics,model_level,levels)