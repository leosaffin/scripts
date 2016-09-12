import tropopause
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from mymodule import forecast, convert, diagnostic, plot
from scripts import case_studies


def main(cubes, dz, names):
    # Calculate the tropopause height
    trop, fold_t, fold_b = tropopause.height(cubes)

    # Mask ridges/troughs
    ridges, troughs = tropopause.ridges_troughs(cubes)

    # Calculate the profiles
    diags = convert.calc(names, cubes)
    profile = diagnostic.profile(diags, trop, dz, mask=troughs)

    # Plot the figures
    plot.multiline(profile, profile[0].coords()[0])
    plt.figure(1)
    plt.axvline(color='k')
    plt.axhline(color='k')
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    dz = np.linspace(-2000, 2000, 21)

    names = ['long_wave_radiation_pv', 'microphysics_pv', 'boundary_layer_pv',
             'dynamics_tracer_inconsistency', 'total_minus_advection_only_pv']

    main(cubes, dz, names)
