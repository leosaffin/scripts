import numpy as np
from irise import convert, diagnostic, grid
from irise.detection import rossby_waves


def ridges_troughs(cubes):
    thetapv2 = convert.calc('air_potential_temperature', cubes,
                            levels=('ertel_potential_vorticity', [2]))[0]

    ridges, troughs = rossby_waves.make_nae_mask(thetapv2, year=2009)

    return ridges, troughs


def height(cubes):
    # Calculate the tropopause height
    pv = convert.calc('ertel_potential_vorticity', cubes)
    q = convert.calc('specific_humidity', cubes)
    trop, fold_t, fold_b = diagnostic.dynamical_tropopause(pv, q)

    return trop, fold_t, fold_b


def mask(cubes):
    """Makes a mask to ignore the boundary layer and far from the tropopause
    """
    pv = convert.calc('ertel_potential_vorticity', cubes)
    q = convert.calc('specific_humidity', cubes)
    mask = np.logical_not(diagnostic.tropopause(pv, q))

    return mask
