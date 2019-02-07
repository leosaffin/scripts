import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from irise import convert, diagnostic, variable
from myscripts.models.um import case_studies
import tropopause

pvtrop = 3.5
pvname = 'ertel_potential_vorticity'
dz = np.linspace(-2000, 2000, 21)


def main(cubes):
    """
    """
    # Calulate N^2
    theta = convert.calc('air_potential_temperature', cubes)
    nsq = variable.N_sq(theta)

    # Find the tropopause
    ztrop, fold_t, fold_b = tropopause.height(cubes)

    # Mask ridges and troughs
    ridges, troughs = tropopause.ridges_troughs(cubes)

    # Create profile of N_sq vs tropopause
    for name, mask in [('troughs', ridges), ('ridges', troughs)]:
        cube = diagnostic.profile(nsq, ztrop, dz, mask=mask)[0]
        iplt.plot(cube, cube.coords()[0], label=name)

    plt.axhline(color='k')
    plt.xlabel(r'$N^2$ $s^{-1}$')
    plt.ylabel('Distance from the tropopause')
    plt.legend(loc='best')
    plt.title('Tropopause PV = %.1f' % pvtrop)
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
