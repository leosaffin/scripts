"""
Find when the difference between ensembles of different precision is
significant.
"""
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from iris.analysis import MEAN
from myscripts.statistics import rms_diff
from myscripts.models.speedy import datadir


def main():
    # Parameters
    path = datadir + 'stochastic/ensembles/'
    variable = 'Temperature'
    # pressure = [925, 850, 700, 500, 300, 200, 100, 30]
    pressure = 500

    # Load the ensembles
    cs = iris.Constraint(variable, pressure=pressure)
    fp = iris.load_cube(path + 'rp_physics_52b_v3.nc', cs)
    fp = fp.collapsed('ensemble_member', MEAN)

    # Compare the ensembles
    for exp in ['convection_8b', 'surface_fluxes_8b', 'vertical_diffusion_8b',
                'physics_8b', 'physics_10b', 'physics_23b', 'physics_52b', 'physics_52b_v2']:
        rp = iris.load_cube(path + 'rp_{}.nc'.format(exp), cs)
        rp = rp.collapsed('ensemble_member', MEAN)
        error = rms_diff(rp, fp)

        # Plot the differences
        qplt.plot(error, label=exp)

    plt.legend()
    plt.show()

    return


if __name__ == '__main__':
    main()
