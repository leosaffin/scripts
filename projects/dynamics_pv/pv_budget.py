import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from myscripts import case_studies


levels = ('air_potential_temperature', [320])
clevs = plot.even_cscale(2)
cmap = 'coolwarm'


def main(cubes):
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    adv = convert.calc('advection_only_pv', cubes, levels=levels)[0]
    for n, name in enumerate(['sum_of_physics_pv_tracers', 'epsilon',
                              'dynamics_tracer_inconsistency', 'residual_pv']):
        cube = convert.calc(name, cubes, levels=levels)[0]

        m = n / 2
        ax = plt.subplot2grid((2, 2), (n - 2 * m, m))
        iplt.contourf(cube, clevs, cmap=cmap)
        plot._add_map()
        iplt.contour(pv, [2], colors='k', linestyles='-')
        iplt.contour(adv, [2], colors='k', linestyles='-')

    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
