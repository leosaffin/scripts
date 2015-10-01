"""The PV dipole plot
"""

import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid, diagnostic, plot


def main(filenames, varnames, bins):
    """
    """
    # Load the data
    pv1, pv2, q, mass, surf, variables = load(filenames, varnames)

    # Calculate the diagnostic
    means, masses = calculate(pv1, pv2, q, mass, surf, variables)

    # Save the data

    # Plot the data
    plotfig(means, masses, bins, varnames)


def load(filenames, varnames):
    """ Extracts required fields from the file
    """
    # Load the data
    cubelist = files.load(filenames)

    # Extract relevant variables
    cubelist.remove(cubelist.extract('air_pressure')[0])
    pv1 = convert.calc('advection_only_pv', cubelist)
    pv2 = convert.calc('advection_only_pv', cubelist)
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

    return pv1, pv2, q, mass, surf, variables


def calculate(pv1, pv2, q, mass, surf, variables):
    # Make a tropopause masked
    trop = diagnostic.tropopause2(pv1, q, qmax=0.001)

    mask = surf.data * np.ones(pv1.shape) > pv1.coord('altitude').points
    mask = np.logical_or(np.logical_not(trop), mask)
    means, masses = diagnostic.averaged_over(variables, bins, pv2.data,
                                             mass, mask=mask)

    return means, masses


line = ['-xk', '--xk', ':xk', '-.xk']


def plotfig(means, masses, bins, varnames):
    bin_centres = 0.5 * (bins[0:-1] + bins[1:])
    for n, mean in enumerate(means):
        plot.dipole(bin_centres, mean, line[n], linewidth=2, ms=5, mew=2,
                    label=varnames[n].replace('_', ' '))
    plt.axis([0, 8, -0.25, 0.25])
    plt.legend(loc='best')
    plt.savefig('/home/lsaffi/plots/iop5/dipole/36h_adv_dipole.png')
    plt.clf()
    plt.bar(bins[0:-1], masses, width=bins[1] - bins[0])
    plt.ylabel('Mass (kg)')
    plt.xlabel('Advection Only PV (PVU)')
    plt.savefig('/home/lsaffi/plots/iop5/dipole/36h_mass.png')

if __name__ == '__main__':
    binmin = 0.0
    binmax = 8.0
    binspace = 0.25
    nbins = int((binmax - binmin) / binspace) + 1
    bins = np.linspace(binmin, binmax, nbins)

    filenames = '/projects/diamet/lsaffi/xjjhq/xjjhqa_036.pp'

    variables = ['total_minus_advection_only_pv',
                 'sum_of_physics_pv_tracers',
                 'dynamics_tracer_inconsistency',
                 'residual_pv']
    main(filenames, variables, bins)
