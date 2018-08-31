#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from mymodule import convert, grid
from mymodule.user_variables import plotdir
from mymodule.detection import rossby_waves
from mymodule.detection.rossby_waves import tropopause_contour as tropoc
from myscripts.models.um import case_studies

cmap = mpl.colors.ListedColormap(
    ['white', 'grey', 'red', 'blue', 'cyan', 'magenta', 'green'])

pv_trop = 2
theta = 300


def main(cubes):
    # Read potential vorticity at 320-K isentropic surface
    pv = convert.calc('ertel_potential_vorticity', cubes,
                      levels=('air_potential_temperature', [theta]))[0]

    # Set coordinate with north pole in the centre
    lon, lat = grid.true_coords(pv)
    xp = (90 - lat) * np.sin(lon * np.pi / 180)
    yp = - (90 - lat) * np.cos(lon * np.pi / 180)

    time = grid.get_datetime(pv)
    eqlat = rossby_waves.equivalent_latitude(time, theta, pv_trop).data

    # Find the contour of 2 PVU that wraps around the globe
    cs = plt.contour(xp, yp, pv.data, [pv_trop])
    contours_fct = tropoc.get_contour_verts(cs)
    tropopause_contour = tropoc.get_tropopause_contour(contours_fct[0])

    if tropoc.is_closed_contour(tropopause_contour):
        # if tropoc.is_closed_contour(tropopause_contour):
        path = Path(tropopause_contour)
        points = np.transpose(np.array([xp.flatten(), yp.flatten()]))
        inside = np.reshape(path.contains_points(points), pv.shape)

        # Create a category map
        vortex = np.logical_and(
            inside, np.logical_and(lat > eqlat, pv.data > pv_trop))
        ridge = np.logical_and(
            np.logical_not(inside), np.logical_and(lat > eqlat,
                                                   pv.data < pv_trop))
        trough = np.logical_and(
            inside,  np.logical_and(lat < eqlat, pv.data > pv_trop))
        cut_off = np.logical_and(np.logical_not(inside), pv.data > pv_trop)
        cut_on = np.logical_and(inside, pv.data < pv_trop)

        cat_map = (vortex.astype(int) +
                   2 * ridge.astype(int) +
                   3 * trough.astype(int) +
                   4 * cut_off.astype(int) +
                   5 * cut_on.astype(int))
        plt.clf()
        plt.pcolormesh(xp, yp, cat_map, vmin=0, vmax=6, cmap=cmap)
        plt.contour(xp, yp, pv.data, [2], colors='k')
        plt.plot(tropopause_contour[:, 0], tropopause_contour[:, 1], color='w')

        # Add land mask
        z = convert.calc('altitude', cubes)
        land = z[0].data != 20
        plt.contour(xp, yp, land, [0.5], colors='k', linewidths=1)
        plt.xlim(-60, 60)
        plt.ylim(-60, 60)
        plt.savefig(plotdir + 'output/' + 'category_map_pv2_theta' +
                    str(theta) + '.png')

    else:
        plt.clf()
        plt.plot(tropopause_contour[:, 0], tropopause_contour[:, 1])
        print('Open contour')

    plt.show()

    return ridge

if __name__ == '__main__':
    forecast = case_studies.iop5_global.copy()
    cubes = forecast.set_lead_time(hours=48)
    main(cubes)
