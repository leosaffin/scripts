from datetime import timedelta as dt
import numpy as np
from mymodule import convert, grid, diagnostic, files
from scripts import case_studies


def main(forecast, times, names):
    for n, time in enumerate(times):
        print(time)
        cubes = forecast.set_lead_time(time)

        # Load required variables
        pv = convert.calc('advection_only_pv', cubes)
        q = convert.calc('specific_humidity', cubes)
        surf = convert.calc('atmosphere_boundary_layer_height', cubes)
        cubes.append(grid.volume(pv))
        mass = convert.calc('mass', cubes)

        # Make a tropopause and boundary layer mask
        mask = make_mask(pv, q, surf)

        # Calculate the tropopause dipole for each diagnostic
        diags = convert.calc(names)
        output = diagnostic.averaged_over(diags, bins, pv, mass, mask=mask)

        files.save(output, path + str(n).zfill(3) + '.nc')

    return


def make_mask(pv, q, surf):
    """Makes a mask to ignore the boundary layer and far from the tropopause
    """
    trop = diagnostic.tropopause(pv, q)
    mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    mask = np.logical_or(np.logical_not(trop), mask)

    return mask


if __name__ == '__main__':
    names = ['total_minus_advection_only_pv']
    bins = np.linspace(0, 8, 33)
    times = [dt(hours=n) for n in range(1, 37)]
    forecast = case_studies.iop8()
    path = '/home/lsaffi/data/iop8/dipole/acc_dipole_'
    main(forecast, times, names)
