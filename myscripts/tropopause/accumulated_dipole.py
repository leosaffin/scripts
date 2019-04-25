import numpy as np
from irise import convert, grid, diagnostics

from myscripts import datadir
from myscripts.models.um import case_studies


def main():
    path = datadir + 'iop8/dipole/acc_dipole_'
    forecast = case_studies.iop8.copy()
    names = ['total_minus_advection_only_pv']
    bins = np.linspace(0, 8, 33)

    calc_dipole(forecast, names, bins, path)

    return


def calc_dipole(forecast, names, bins, path):
    # Loop over all lead times in the forecast
    for n, cubes in enumerate(forecast):
        print(n)

        # Load required variables
        pv = convert.calc('advection_only_pv', cubes)
        cubes.append(grid.volume(pv))
        mass = convert.calc('mass', cubes)

        # Make a tropopause and boundary layer mask
        raise NotImplementedError('Tropopause Mask')

        #mask = tropopause.mask(cubes)

        # Calculate the tropopause dipole for each diagnostic
        #diags = convert.calc(names)
        #output = diagnostics.averaged_over(diags, bins, pv, mass, mask=mask)

        #iris.save(output, path + str(n).zfill(3) + '.nc')
    return


if __name__ == '__main__':
    main()
