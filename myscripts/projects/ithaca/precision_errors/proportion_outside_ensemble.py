"""
Find when a forecast is more than one standard deviation away from the ensemble
mean. For a Gaussian distribution this is expected to be 1/3 of points. Check
this criteria for reduced precision ensembles
"""
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
from iris.analysis import MEAN, STD_DEV
from myscripts.statistics import global_mean
from myscripts.models.speedy import datadir


def main():
    # Parameters
    path = datadir + 'stochastic/ensembles/'
    variable = 'Geopotential Height'

    # List of ensembles to compare
    experiments = [
        'convection_8b', 'surface_fluxes_8b', 'vertical_diffusion_8b',
        'physics_8b', 'physics_10b', 'physics_23b',
        'physics_52b', 'physics_52b_v2', 'physics_52b_v3']

    # Load the ensembles
    cs = iris.Constraint(variable)

    # Reference ensemble
    fp = iris.load_cube(path + 'rp_physics_52b.nc', cs)
    fp_mean = fp.collapsed('ensemble_member', MEAN)
    fp_spread = fp.collapsed('ensemble_member', STD_DEV, ddof=1)

    # Compare the ensembles
    for exp in experiments:
        rp = iris.load_cube(path + 'rp_{}.nc'.format(exp), cs)

        proportion = proportion_different(rp, fp_mean, fp_spread)

        # Plot the differences
        qplt.plot(proportion, label=exp)

    plt.legend()
    plt.show()

    return


def proportion_different(ensemble, mean, spread):
    """Calculate the proportion of gridboxes that lie outside 1 standard
    deviation of the ensemble from the ensemble mean
    """
    # Create a 1's and 0's cube of which gridboxes lie outside
    n_out = np.logical_or(ensemble.data > mean.data + spread.data,
                          ensemble.data < mean.data - spread.data)
    n_out = ensemble.copy(data=n_out)

    # Collapse the cube to get an average proportion
    proportion = global_mean(n_out)
    proportion = proportion.collapsed(['ensemble_member', 'pressure'], MEAN)

    return proportion


if __name__ == '__main__':
    main()
