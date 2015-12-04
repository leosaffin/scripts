import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import files, convert, grid, plot
from scripts.pv_on_theta import cube_on_level


def main(cubes, rdf_pv, p_value, cscale):
    # Extract a pressure coordinate
    p = convert.calc('air_pressure', cubes)
    p = grid.make_coord(p)

    # Calculate required variables
    pv = cube_on_level('ertel_potential_vorticity', cubes, p, p_value)
    adv = cube_on_level('advection_only_pv', cubes, p, p_value)
    qsum = cube_on_level('sum_of_physics_pv_tracers', cubes, p, p_value)

    # Calculate the residuals
    epsilon = pv - adv - qsum
    epsilon.rename('epsilon')

    # Residual with rdf PV
    epsilon_rdf = pv.data - rdf_pv.data - qsum.data
    epsilon_rdf = np.ma.masked_where(epsilon_rdf < -10, epsilon_rdf)
    epsilon_rdf = epsilon.copy(data=epsilon_rdf)
    epsilon_rdf.rename('epsilon_rdf')

    # Plot both figures
    for cube in [epsilon, epsilon_rdf]:
        plt.figure()
        plot.contourf(cube, cscale, cmap='bwr', extend='both')

        # Add positive and negative lines
        iplt.contour(cube, [cscale[len(cscale) / 2]],
                     colors='k', linestyles='-')
        iplt.contour(cube, [cscale[len(cscale) / 2 - 1]],
                     colors='k', linestyles='--')

    plt.show()

if __name__ == '__main__':
    rdf_pv = files.load('/home/lsaffi/data/iop5/trajectories/' +
                        'rdf_pv_500hpa_35h.nc')[0]
    cubes = files.load('/projects/diamet/lsaffi/xjjhq/xjjhqa_035.pp')
    main(cubes, rdf_pv, 50000, plot.even_cscale(2))
