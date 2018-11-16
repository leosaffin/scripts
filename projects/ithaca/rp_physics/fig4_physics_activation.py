"""
Need to consider the switching on and off of physics schemes with reduced
precision. Show the active/deactive points as a function of precision for
selected physics schemes (Vertical Diffusion/Surface Fluxes/Convection)
"""

import matplotlib.pyplot as plt
import iris
from myscripts.projects.ithaca.tendencies.number_activated \
    import plot_active
from myscripts.models.speedy import datadir


def main():
    # Load cubes
    path = datadir + 'deterministic/'
    cs = iris.Constraint(
        cube_func=lambda x: 'Temperature Tendency' in x.name(),
        forecast_period=2/3, pressure=0.95)
    rp_cubes = iris.load(path + 'rp_*_tendencies.nc', cs)
    fp_cubes = iris.load(path + 'fp_tendencies.nc', cs)

    # Create a two by two grid with shared x and y axes along rows and columns
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True,
                             figsize=[12.0, 7.2])

    plt.axes(axes[0, 0])

    plt.axes(axes[0, 1])
    scheme = 'Vertical Diffusion'
    make_plot(rp_cubes, fp_cubes, scheme)
    plt.legend(title='Number of gridpoints')

    plt.axes(axes[1, 0])
    scheme = 'Surface Fluxes'
    make_plot(rp_cubes, fp_cubes, scheme)

    plt.axes(axes[1, 1])
    scheme = 'Convection'
    make_plot(rp_cubes, fp_cubes, scheme)

    plt.show()

    return


def make_plot(rp_cubes, fp_cubes, scheme):
    plt.title(scheme)
    name = 'Temperature Tendency due to {} [K/s]'.format(scheme)
    rp = rp_cubes.extract_strict(iris.Constraint(name))
    fp = fp_cubes.extract_strict(iris.Constraint(name))
    plot_active(rp, fp)

    return


if __name__ == '__main__':
    main()
