from datetime import timedelta as dt
import numpy as np
import iris
from iris.analysis import MEAN, STD_DEV
from mymodule import convert, grid, files
from myscripts import case_studies


def main(forecast, diagnostics, lead_times):
    for n, lead_time in enumerate(lead_times):
        print(n)
        cubes = forecast.set_lead_time(lead_time)

        # Extract required variables
        x = convert.calc(diagnostics, cubes)
        surf = convert.calc('atmosphere_boundary_layer_height', cubes)
        pv = convert.calc('total_pv', cubes)
        q = convert.calc('specific_humidity', cubes)
        cubes.append(grid.volume(pv))
        mass = convert.calc('mass', cubes)

        mask = make_mask(surf, pv, q)
        output = calculate(x, mass, mask)

        files.save(output, str(n).zfill(3) + '.nc')

    return


def calculate(x, mass, mask):
    output = iris.cube.CubeList()
    for cube in x:
        xcoord = grid.extract_dim_coord(cube, 'X')
        ycoord = grid.extract_dim_coord(cube, 'Y')
        zcoord = grid.extract_dim_coord(cube, 'Z')
        cube.data = np.ma.masked_where(mask, cube.data)
        output.append(cube.collapsed([xcoord, ycoord, zcoord], MEAN,
                                     weights=mass.data))
        output.append(cube.collapsed([xcoord, ycoord, zcoord], STD_DEV))

    return output


def make_mask(surf, pv, q):
    bl = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    stratosphere = np.logical_and(pv.data > 2.0, q.data < 0.001)
    mask = np.logical_or(bl, stratosphere)

    return mask


if __name__ == '__main__':
    forecast = case_studies.iop5()
    lead_times = [dt(n) for n in xrange(0, 37)]
    diagnostics = ['short_wave_radiation_pv',
                   'long_wave_radiation_pv',
                   'microphysics_pv',
                   'gravity_wave_drag_pv',
                   'convection_pv',
                   'boundary_layer_pv',
                   'dynamics_tracer_inconsistency',
                   'cloud_rebalancing_pv',
                   'total_minus_advection_only_pv',
                   'sum_of_physics_pv_tracers',
                   'residual_pv']
    main(forecast, diagnostics, lead_times)
