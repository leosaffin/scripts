from irise import convert
from irise.diagnostics import rossby_waves, tropopause


def ridges_troughs(cubes):
    thetapv2 = convert.calc('air_potential_temperature', cubes,
                            levels=('ertel_potential_vorticity', [2]))[0]

    ridges, troughs = rossby_waves.make_nae_mask(thetapv2, year=2009)

    return ridges, troughs


def height(cubes):
    # Calculate the tropopause height
    pv = convert.calc('ertel_potential_vorticity', cubes)
    q = convert.calc('specific_humidity', cubes)
    trop, fold_t, fold_b = tropopause.dynamical(pv, q)

    return trop, fold_t, fold_b
