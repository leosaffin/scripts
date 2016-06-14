from datetime import timedelta as dt
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import files, convert, grid, plot
from scripts import case_studies


def main(cubes, rdf_pv, p_level, *args, **kwargs):
    # Calculate required variables
    pv = convert.calc('ertel_potential_vorticity', cubes,
                      levels=('air_pressure', [p_level]))[0]
    adv = convert.calc('advection_only_pv', cubes,
                       levels=('air_pressure', [p_level]))[0]
    qsum = convert.calc('sum_of_physics_pv_tracers', cubes,
                        levels=('air_pressure', [p_level]))[0]

    diff = pv - qsum
    diff.rename('pv_minus_physics_pv_tracers')

    # Plot both figures
    for cube in [diff, adv, rdf_pv]:
        plt.figure()
        plot.contourf(cube, *args, **kwargs)

    plt.show()

if __name__ == '__main__':
    rdf_pv = files.load('/home/lsaffi/data/iop5/trajectories/' +
                        'rdf_pv_500hpa_35h.nc')[0]
    forecast = case_studies.iop5b()
    cubes = forecast.set_lead_time(dt(hours=35))
    main(cubes, rdf_pv, 50000, np.linspace(0, 2, 9),
         cmap='cubehelix_r', extend='both')
