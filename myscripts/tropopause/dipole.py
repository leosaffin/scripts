"""The PV dipole plot
"""
import numpy as np
import matplotlib.pyplot as plt
from irise import convert, grid, diagnostics, plot
from myscripts.models.um import case_studies
import tropopause


def main(cubes, varnames, bins):
    # Load the data
    q_adv = convert.calc('advection_only_pv', cubes)
    density = convert.calc('air_density', cubes)

    volume = grid.volume(q_adv)
    mass = density * volume
    mass.rename('mass')
    x = convert.calc(varnames, cubes)

    # Mask away from the tropopause
    mask = tropopause.mask(cubes)

    # Calculate the diagnostic
    means = diagnostics.averaged_over(x, bins, q_adv, mass, mask)

    # Plot the data
    means.remove(convert.calc('mass', means))
    plot.multiline(means)
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    bins = np.linspace(0, 8, 33)

    variables = ['total_minus_advection_only_pv',
                 'sum_of_physics_pv_tracers',
                 'dynamics_tracer_inconsistency',
                 'residual_pv']
    main(cubes, variables, bins)
