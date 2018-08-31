from datetime import timedelta as dt
import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, plot
from mymodule.user_variables import datadir
from myscripts.models.um import case_studies


def main():
    rdf_pv = files.load(datadir + 'iop5/trajectories/rdf_pv_500hpa_35h.nc')[0]
    forecast = case_studies.iop5b()
    cubes = forecast.set_lead_time(dt(hours=35))
    compare_pv(cubes, rdf_pv, 50000, np.linspace(0, 2, 9),
               cmap='cubehelix_r', extend='both')
    plt.show()

    return


def compare_pv(cubes, rdf_pv, p_level, *args, **kwargs):
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

    return


if __name__ == '__main__':
    main()
