"""The PV dipole plot
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import files, convert, grid, diagnostic, plot


def main(filenames, varnames, bins):
    """
    """
    # Load the data
    pv, q, mass, surf, variables = load(filenames, varnames)

    # Calculate the diagnostic
    means = calculate(pv, q, mass, surf, variables)

    # Save the data

    # Plot the data
    plotfig(means, bins, varnames)
    plt.savefig('dipole.png')


def load(filenames, varnames):
    """ Extracts required fields from the file
    """
    # Load the data
    cubelist = files.load(filenames)

    # Extract relevant variables
    cubelist.remove(cubelist.extract('air_pressure')[0])
    pv = convert.calc('advection_only_pv', cubelist)
    q = convert.calc('specific_humidity', cubelist)

    # Calculate the mass in each gridbox
    density = convert.calc('air_density', cubelist)
    volume = grid.volume(density)
    mass = volume * density.data

    # Calculate lower boundary
    surf = (convert.calc('surface_altitude', cubelist) +
            convert.calc('atmosphere_boundary_layer_thickness', cubelist))

    # Extract other diagnostics
    variables = [convert.calc(name, cubelist).data for name in varnames]

    return pv, q, mass, surf, variables


def calculate(pv, q, mass, surf, variables):
    # Make a tropopause masked
    trop = diagnostic.tropopause2(pv, q)
    mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    mask = np.logical_or(trop, mask)

    means = []
    for variable in variables:
        means.append(diagnostic.averaged_over(variable, bins, pv.data, mass,
                                              mask=mask))
    return means


def plotfig(means, bins, varnames):
    bin_centres = 0.5 * (bins[0:-1] + bins[1:])
    for mean, name in zip(means, varnames):
        plot.dipole(bin_centres, mean, label=name)
    plt.legend()

if __name__ == '__main__':
    binmin = 0.0
    binmax = 8.0
    binspace = 0.25
    nbins = int((binmax - binmin) / binspace) + 1
    bins = np.linspace(binmin, binmax, nbins)

    filenames = '/projects/diamet/lsaffi/xjjhq/xjjha_036.pp'

    variables = ['total_minus_advection_only_pv', 'sum_of_physics_pv_tracers']
    main(filenames, variables, bins)
