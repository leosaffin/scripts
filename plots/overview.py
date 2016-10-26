import os
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from scripts import case_studies

# Vertical coordinates
# Inlcude each coordinate interpolated to the other coordinates
# Altitude - Surface, 10m, 5km, 8km, 10km, 12km
# Pressure - 950 hPa, 850hPa, 700hPa, 500hPa, 300hPa, 200hPa, 150hPa
# Potential Temperature - 300K, 310K, 320K, 330K, 340K, 350K

levels = [('altitude', [100, 5000, 8000, 10000, 12000]),
          ('air_pressure', [95000, 85000, 70000, 50000, 30000, 20000, 15000]),
          ('air_potential_temperature', [300, 310, 320, 325, 330, 340, 350]),
          ('ertel_potential_vorticity', [2])]

# Single Level Fields
# MSLP, Rainfall, Total Column Water, BL Depth
single_level_fields = ['atmosphere_boundary_layer_thickness',
                       'convective_rainfall_amount',
                       'stratiform_rainfall_amount',
                       'air_pressure_at_sea_level']


# Multi-level Fields
# T, theta_w, u, v, w, divergence, vorticity, q, q_cl, q_cf, RH, PV tracers
multi_level_fields = ['air_temperature',
                      'wind_speed',
                      'upward_air_velocity',
                      'specific_humidity',
                      'mass_fraction_of_cloud_liquid_water_in_air',
                      'mass_fraction_of_cloud_ice_in_air',
                      'relative_humidity']

tracers = ['short_wave_radiation_pv',
           'long_wave_radiation_pv',
           'microphysics_pv',
           'gravity_wave_drag_pv',
           'convection_pv',
           'boundary_layer_pv',
           'cloud_rebalancing_pv',
           'dynamics_tracer_inconsistency',
           'residual_pv']

directory = '/home/lsaffin/Documents/meteorology/output/iop8/overview/'


def main(cubes):
    for name, values in levels:
        os.system('mkdir ' + directory + name)
        for field in multi_level_fields:
            make_plots(field, cubes, name, values)
        for field, dummy in levels:
            if field != name:
                make_plots(field, cubes, name, values)


def make_plots(field, cubes, name, values):
    cube = convert.calc(field, cubes, levels=(name, values))
    for n, level in enumerate(values):
        plot.pcolormesh(cube[n], vmin=-2, vmax=2, cmap='coolwarm')
        plt.savefig(directory + name + '/' + field + '_' + str(level) + '.png')
        plt.clf()


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
