"""Plot the number of grid boxes diagnosed to be modified by a physics scheme
as a function of precision.
"""
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from iris.util import squeeze
from myscripts.statistics import count
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/'
    scheme = 'Vertical Diffusion'
    string = 'Temperature Tendency due to'
    lead_time = 2 / 3
    pressure = 0.95
    min_tend = 1e-6

    cs = iris.Constraint(cube_func=lambda x: string in x.name(),
                         forecast_period=lead_time,
                         pressure=pressure)
    filename = 'rp_{}_tendencies.nc'.format(scheme.lower().replace(' ', '_'))
    cube = iris.load_cube(path + filename, cs)

    plot_active(cube, threshold=min_tend)
    plt.xlabel('Precision (sbits)')
    plt.ylabel('Number of active gridpoints')
    plt.title(scheme)
    plt.show()

    return


def plot_active(cube, threshold=0., **kwargs):
    # Count the number of gridboxes with nonzero tendencies
    nactive = squeeze(count(cube, func=lambda x: abs(x) >= threshold))
    iplt.plot(nactive, **kwargs)

    return


if __name__ == '__main__':
    main()
