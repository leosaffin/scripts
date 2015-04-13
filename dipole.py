"""The PV dipole plot
"""

import numpy as np
import matplotlib.pyplot as plt
from mymodule import load, convert, grid, diagnostic


def main(files, variables):
    """
    """
    mean = {}

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

    for variable in variables:
        data = convert.calc_tracer(cubelist, variable).data
        data = np.ma.masked_where(tropopause, data)
        mean[variable] = diagnostic.averaged_over(data, bins, pv.data,
                                                  weights=mass)
    # Save the data

    # Plot the data
    for variable in variables:
        plt.plot(mean[variable], label=variable)

    plt.savefig('dipole.png')

if __name__ == '__main__':
    binmin = 0.0
    binmax = 8.0
    binspace = 0.25
    bins = []
    for n in xrange(int(binmax / binspace)):
        bins.append([binmin + binspace * n, binmin + binspace * (n + 1)])
    files = []
    prefix = '/projects/diamet/lsaffi/xjjhq/xjjhqa_p'
    suffixes = ['a030', 'b030']
    for suffix in suffixes:
        files.append(prefix + suffix)
    variables = ['total_minus_advection_only_pv']
    main(files, variables)
