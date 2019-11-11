import numpy as np


def rearrange(cube):
    """
    SPEEDY stores spectral data in a stange layout. Rearrange to total
    wavenumber vs zonal wavenumber
    """
    nx = cube.shape[-2]
    mx = cube.shape[-1]

    x = cube.copy(data=np.zeros_like(cube.data))
    x.coord('longitude').rename('total_wavenumber')
    x.coord('latitude').rename('zonal_wavenumber')
    for n in range(nx):
        for m in range(mx):
            l = m + n
            if l < mx:
                x.data[..., n, l] = cube.data[..., n, m]

    return x
