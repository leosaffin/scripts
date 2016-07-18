"""The PV dipole plot
"""
import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, grid, diagnostic, interpolate, plot
from mymodule.detection import rossby_waves
from scripts import case_studies


def main(cubes, varnames, bins):
    # Load the data
    q_adv = convert.calc('advection_only_pv', cubes)
    pv = convert.calc('advection_only_pv', cubes)
    q = convert.calc('specific_humidity', cubes)
    cubes.append(grid.volume(pv))
    mass = convert.calc('mass', cubes)
    x = convert.calc(varnames, cubes)

    # Mask away from the tropopause
    mask = diagnostic.tropopause(pv, q)
    mask = np.logical_not(mask)
    # Calculate the diagnostic
    means = diagnostic.averaged_over(x, bins, q_adv, mass, mask)

    # Plot the data
    means.remove(convert.calc('mass', means))
    plot.multiline(means)
    plt.show()


def from_cubelist(cubes, **kwargs):
    names = []

    # Extract variables from the cubelist
    pv = convert.calc('advection_only_pv')
    tracers = convert.calc(names, cubes)

    # Calculate the tropopause altitude
    grid.add_hybrid_height(pv)
    z = grid.make_cube(pv, 'altitude')
    zpv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    # Mask troughs
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('ertel_potential_vorticity', [2]))[0]
    ridges, troughs = rossby_waves.make_nae_mask(theta)

    # Calculate the diagnostic
    dz = kwargs['dz']
    output = diagnostic.profile(tracers, zpv2, dz, mask=troughs)

    return output

if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(hours=36)
    bins = np.linspace(0, 8, 33)

    variables = ['total_minus_advection_only_pv',
                 'sum_of_physics_pv_tracers',
                 'dynamics_tracer_inconsistency',
                 'residual_pv']
    main(cubes, variables, bins)
