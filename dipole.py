"""The PV dipole plot
"""

import numpy as np
import matplotlib.pyplot as plt
from mymodule import io, convert, grid, diagnostic, plot


def main(files, variables, bins):
    """
    """
    # Load the data
    cubelist = io.load(files)
    cubelist.remove(cubelist.extract('air_pressure')[0])
    pv = convert.calc('advection_only_pv', cubelist)

    # Calculate the mass in each gridbox
    density = convert.calc('air_density', cubelist)
    volume = grid.volume(density)
    mass = volume * density.data

    # Make a tropopause masked
    q = convert.calc('specific_humidity', cubelist)
    tropopause = diagnostic.tropopause(pv.data, q.data)

    mean = {}
    for variable in variables:
        x = convert.calc(variable, cubelist).data
        mean[variable] = diagnostic.averaged_over(x, bins, pv.data,
                                                  mass,
                                                  mask=tropopause)
    # Save the data

    # Plot the data
    bin_centres = 0.5 * (bins[0:-1] + bins[1:])
    for variable in variables:
        plot.dipole(bin_centres, mean[variable], label=variable)

    plt.legend()
    plt.savefig('dipole.png')

if __name__ == '__main__':
    binmin = 0.0
    binmax = 8.0
    binspace = 0.25
    nbins = int((binmax - binmin) / binspace) + 1
    bins = np.linspace(binmin, binmax, nbins)

    files = '/projects/diamet/lsaffi/season/*054.pp'

    variables = ['total_minus_advection_only_pv', 'sum_of_physics_pv_tracers']
    main(files, variables, bins)
