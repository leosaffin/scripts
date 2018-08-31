import numpy as np
import matplotlib.pyplot as plt
from iris.analysis import Linear
from mymodule import calculus, convert, diagnostic, grid, interpolate, plot, \
    variable

from mymodule.detection import rossby_waves
from myscripts.models.um import case_studies

names = ['long_wave_radiation_pv', 'total_minus_advection_only_pv',
         'advection_only_pv', 'ertel_potential_vorticity']


def main(cubes, dz):
    # Calculate dp/dz (Hydrostatic balance dp/dz = -\rho g
    P = convert.calc('air_pressure', cubes)
    z = grid.make_cube(P, 'altitude')
    dP_dz = calculus.multidim(P, z, 'z')
    dP_dz = remap_3d(dP_dz, P)

    # Calculate absolute vorticity
    u = convert.calc('x_wind', cubes)
    v = convert.calc('y_wind', cubes)
    du_dy = calculus.diff_by_axis(u, 'y')
    du_dy = remap_3d(du_dy, P)
    dv_dx = calculus.diff_by_axis(v, 'x')
    dv_dx = remap_3d(dv_dx, P)
    vort = du_dy.data - dv_dx.data

    lat = grid.true_coords(P)[1]
    abs_vort = 2 * convert.omega.data * np.cos(lat) * vort

    # Calculate Nsq for each PV tracer
    tracers = convert.calc(names, cubes)
    nsq_0 = variable.N_sq(convert.calc('air_potential_temperature', cubes))
    nsq = []
    nsq.append(nsq_0)
    for tracer in tracers:
        nsq_i = -1 * tracer * dP_dz / abs_vort
        nsq_i.rename(tracer.name())
        nsq.append(nsq_i)

    # Create an average profile
    thetapv2 = convert.calc('air_potential_temperature', cubes,
                            levels=('ertel_potential_vorticity', [2]))
    ridges, troughs = rossby_waves.make_nae_mask(thetapv2)
    pv = grid.make_coord(convert.calc('advection_only_pv', cubes))
    z.add_aux_coord(pv, [0, 1, 2])
    zpv = interpolate.to_level(z, advection_only_pv=[3.5])[0]
    y = diagnostic.profile(nsq, zpv, dz, mask=troughs)

    # Plot nsq

    plot.multiline(y)
    plt.show()


def remap_3d(cube, target):
    cube = cube.regrid(target, Linear())
    cube = cube.interpolate(
        [('level_height', target.coord('level_height').points)], Linear())

    return cube

if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(hours=36)
    dz = np.linspace(-4000, 4000, 21)
    main(cubes, dz)
