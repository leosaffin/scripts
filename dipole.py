"""The PV dipole plot
"""

import numpy as np
import matplotlib.pyplot as plt
from mymodule import load, convert, grid, diagnostic, plot


def main(files, variables):
    """
    """
    # Load the data
    cubelist = load.full(files)
    pv = cubelist.extract('advection_only_pv')[0]

    # Calculate the mass in each gridbox
    pressure = cubelist.extract('air_pressure')[1]
    temperature = cubelist.extract('air_temperature')[0]
    density = convert.calc_rho(pressure, temperature)

    # Calculate the volume of each gridbox
    volume = grid.volume(density)
    mass = volume * density.data

    # Make a tropopause masked
    q = cubelist.extract('specific_humidity')[0]
    tropopause = diagnostic.tropopause(pv, q)

    mean = {}
    for variable in variables:
        x = convert.calc_tracer(cubelist, variable).data
        mean[variable] = diagnostic.averaged_over(x, bins, pv.data,
                                                  mass,
                                                  mask=tropopause)
    # Save the data

    # Plot the data
    bin_centres = [0.5 * (edges[0] + edges[1]) for edges in bins]
    for variable in variables:
        plot.dipole(bin_centres, mean[variable])

    plt.savefig('dipole.png')

if __name__ == '__main__':
    binmin = 0.0
    binmax = 8.0
    binspace = 0.25
    bins = np.linspace(binmin, binmax, int(binmax / binspace + 1))

    files = '/projects/diamet/lsaffi/xjjhq/*030'

    variables = ['total_minus_advection_only_pv']
    main(files, variables)
