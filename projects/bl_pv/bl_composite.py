import numpy as np
from scipy.ndimage import filters
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, diagnostic
from mymodule.plot.util import legend
from myscripts.models.um import case_studies
from systematic_forecasts import second_analysis

forecast = case_studies.iop8.copy()

names = [
    'total_minus_advection_only_pv',
    'short_wave_radiation_pv',
    'long_wave_radiation_pv',
    'microphysics_pv',
    'gravity_wave_drag_pv',
    'convection_pv',
    'boundary_layer_pv',
    'dynamics_tracer_inconsistency',
    'residual_pv'
]

dz = np.linspace(-1000, 1000, 21)


def main():
    # Load the variables
    cubes = forecast.set_lead_time(hours=18)
    x = convert.calc(names, cubes)
    surface = convert.calc('boundary_layer_height', cubes)

    # Mask points within 100 gridpoints of land
    z = convert.calc('altitude', cubes)
    zm = filters.maximum_filter(z[0].data, 100)
    mask = zm > 20

    # Interpolate relative to boundary layer height
    output = diagnostic.profile(x, surface, dz, mask=mask)

    # Plot the variables
    for cube in output:
        c = second_analysis.all_diagnostics[cube.name()]
        iplt.plot(cube, cube.coord('distance_from_boundary_layer_height'),
                  color=c.color, linestyle=c.linestyle, label=c.symbol)

    plt.axvline(color='k')
    plt.axhline(color='k')
    legend(key=second_analysis.get_idx, loc='best', ncol=2)

    plt.show()

    return

if __name__ == '__main__':
    main()
