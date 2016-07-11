from datetime import timedelta as dt
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from mymodule import forecast, convert, grid, interpolate
from mymodule.detection import rossby_waves
from scripts import case_studies


def main(cubes, dz, info):
    """
    """
    # Calculate the tropopause height
    pv = convert.calc('ertel_potential_vorticity', cubes)
    z = grid.make_cube(pv, 'altitude')
    z.add_aux_coord(grid.make_coord(pv), [0, 1, 2])
    zpv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    # Create a coordinate for distance from the tropopause
    zdiff = z.data - zpv2.data
    zdiff = z.copy(data=zdiff)
    zdiff.rename('distance_from_tropopause')
    zdiff = grid.make_coord(zdiff)

    # Mask ridges
    thetapv2 = convert.calc('air_potential_temperature', cubes,
                            levels=('ertel_potential_vorticity', [2]))[0]

    background = rossby_waves.nae_map(grid.get_datetime(thetapv2)[0]).data
    dtheta = thetapv2.data - background
    out_of_bounds = np.logical_or(background < 285, background > 350)
    mask = dtheta < 0
    mask = np.logical_or(mask, out_of_bounds)

    for name, linestyle, label in info:
        x = analyse(cubes, zdiff, dz, name, mask)
        iplt.plot(x, x.coord('distance_from_tropopause'), linestyle,
                  label=label)

    plt.title('IOP8: Tropopause Profile in Ridges (T+36h)')
    plt.xlabel(r'$\Delta q$ (PVU)')
    plt.ylabel('Distance From Tropopause (m)')
    plt.axhline(color='k')
    plt.axvline(color='k')
    #plt.xlim(-0.3, 0.3)
    plt.legend(loc='best', ncol=2)
    plt.show()


def analyse(cubes, zdiff, dz, name, mask):
    q = convert.calc(name, cubes)
    q.add_aux_coord(zdiff, [0, 1, 2])
    qdiff = interpolate.to_level(q, distance_from_tropopause=dz)
    qdiff.data = np.ma.masked_where(mask * np.ones_like(qdiff.data),
                                    qdiff.data)
    x = qdiff.collapsed(['grid_longitude', 'grid_latitude'],
                        iris.analysis.MEDIAN)
    return x


if __name__ == '__main__':
    forecast = case_studies.iop8()
    cubes = forecast.set_lead_time(dt(hours=36))
    dz = np.linspace(-2000, 2000, 21)
    info = [('specific_humidity', '-xk', 'Specific Humidity')]
    """
    info = [('total_minus_advection_only_pv', '-xk', r'$q-q_{adv}$'),
            ('sum_of_physics_pv_tracers', '--xk', r'$\sum q_{phys}$'),
            ('dynamics_tracer_inconsistency', ':xk', r'$\epsilon_{I}$'),
            ('residual_pv', '-.xk', r'$\epsilon_{r}$'),
            ('microphysics_pv', '-xb', r'$q_{mic}$'),
            ('short_wave_radiation_pv', '--xr', r'$q_{sw}$'),
            ('long_wave_radiation_pv', ':xr', r'$q_{lw}$'),
            ('gravity_wave_drag_pv', '-xg', r'$q_{gwd}$'),
            ('convection_pv', '--xb', r'$q_{con}$'),
            ('boundary_layer_pv', ':xb', r'$q_{bl}$')]
    """

    main(cubes, dz, info)
