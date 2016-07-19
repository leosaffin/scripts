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
    names = ['dynamics_tracer_inconsistency',
             'long_wave_radiation_pv',
             'boundary_layer_pv',
             'microphysics_pv',
             'convection_pv']

    # Extract variables from the cubelist
    pv = convert.calc('advection_only_pv', cubes)
    tracers = convert.calc(names, cubes)

    # Add altitude to tracers
    for cube in tracers:
        grid.add_hybrid_height(cube)

    # Calculate the tropopause altitude
    grid.add_hybrid_height(pv)
    z = grid.make_cube(pv, 'altitude')
    pv = grid.make_coord(pv)
    z.add_aux_coord(pv, [0, 1, 2])
    zpv2 = interpolate.to_level(z, advection_only_pv=[2])[0]

    # Calculate the diagnostic
    dz = kwargs['dz']
    output = diagnostic.profile(tracers, zpv2, dz)

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
