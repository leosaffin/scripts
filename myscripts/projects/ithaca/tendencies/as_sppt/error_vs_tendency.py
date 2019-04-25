"""
:math:`T = (1+e) \cdot P`

Error in tendency should be proportional to tendency
"""
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from irise.diagnostics import averaged_over

from myscripts.models import speedy
from myscripts.projects.ithaca.tendencies import load_tendency


def main():
    variable = 'Temperature'
    scheme = 'All Parametrizations'
    rp_scheme = 'all_parametrizations'
    reduced_precision = 10
    sigma = speedy.sigma_levels[0]

    rp = load_tendency(
        variable=variable,
        scheme=scheme,
        rp_scheme=rp_scheme,
        sigma=sigma,
        precision=52)

    fp = load_tendency(
        variable=variable,
        scheme=scheme,
        rp_scheme=rp_scheme,
        sigma=sigma,
        precision=reduced_precision)

    error_vs_tendency(rp, fp, np.linspace(-2e-4, 2e-4, 21))

    plt.show()

    return


def error_vs_tendency(rp, fp, bins):
    """Is the error proportional to the tendency (like SPPT)
    """
    # Average of the absolute error in the tendency binned by the double
    # precision tendency
    error = rp - fp
    error.data = np.abs(error.data)
    mask = np.logical_and(fp.data == 0, rp.data == 0)
    y = averaged_over(error, bins, fp, weights=None, mask=mask)

    fig, axes = plt.subplots(2, 1, sharex=True)

    qplt.plot(y[0], 'kx', axes=axes[0])
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Error in Tendency')
    axes[0].set_title('')

    x = y[1].dim_coords[0].points
    dx = x[1] - x[0]
    axes[1].bar(x, y[1].data, width=dx)
    axes[1].set_xlabel('Double-Precision Tendency')
    axes[1].set_ylabel('Number of Gridpoints')
    axes[1].set_title('')

    return


if __name__ == '__main__':
    main()
