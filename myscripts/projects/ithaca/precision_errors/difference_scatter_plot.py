"""
The surface fluxes scheme temperature tendency involves taking the difference between the boundary-layer temperature and
a derived surface temperature. This difference can be quite small in comparison to the temperature itself resulting in
zero tendency at low precision because the two numbers become the same. A scatter plot of the two temperatures
demonstrates this issue.
"""
from math import floor, ceil
import numpy as np
import matplotlib.pyplot as plt
from myscripts import homepath


def main():
    path = homepath + 'programming/speedy-f90/'

    tmin, tmax = scatterplot(path + 'ref_sflx_t.txt', '.k')
    tmin_rp, tmax_rp = scatterplot(path + 'rp_sflx_t.txt', '.r')

    trange = range(tmin, tmax)
    plt.plot(trange, trange, '--y')
    plt.axis('equal')
    plt.xlim(tmin, tmax)
    plt.show()

    return


def scatterplot(filename, *args, **kwargs):
    data = np.genfromtxt(filename)

    # Extract the data
    fmask = data[:, 0]
    tland_surf = data[:, 1]
    tland_bl = data[:, 2]
    tsea_surf = data[:, 3]
    tsea_bl = data[:, 4]

    # Mask where the differences aren't used
    tland_bl = np.ma.masked_where(fmask == 0, tland_bl)
    tsea_bl = np.ma.masked_where(fmask == 1, tsea_bl)

    # Make the scatterplot
    plt.plot(tland_bl, tland_surf, *args, **kwargs)
    plt.plot(tsea_bl, tsea_surf, *args, **kwargs)

    tmin = data[:, 1:].min()
    tmax = data[:, 1:].max()

    return floor(tmin), ceil(tmax)


if __name__ == '__main__':
    main()
