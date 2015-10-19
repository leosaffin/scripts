#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from iris.analysis import cartography
from mymodule import files, convert, grid, interpolate
from mymodule.detection.rossby_waves import tropopause_contour as tropoc

PV_tropo = 2.2401299  # PVU
# Equivalent latitudes (taken from ~sws07om/matlabd/test_category_map.m)
# based on PV = 2.2401299 PVU on 320K isentropic surface
eqlats = [42.8966,   42.7319,   42.5672,   42.4026,   42.2379,   42.0733,
          41.9086,   41.7440,   41.5793,   41.4147,   41.2500,   41.0854,
          40.9207,   40.7560,   40.5914,   40.5264,   40.4614,   40.3963,
          40.3313,   40.2663,   40.2013,   40.1363,   40.0712,   40.0062,
          39.9412,   39.8762,   39.8112,   39.7462,   39.6811,   39.6161,
          39.5511,   39.4861,   39.4211,   39.3561,   39.2910,   39.2260,
          39.1610,   39.0960,   39.0310,   38.9659,   38.9009,   38.8359,
          38.7709,   38.7059,   38.6409,   38.5758,   38.6011,   38.6263,
          38.6516,   38.6768,   38.7021,   38.7273,   38.7526,   38.7778,
          38.8030,   38.8283,   38.8535,   38.8788,   38.9040,   38.9293,
          38.9545,   38.9798,   39.0050,   39.0303,   39.0555,   39.0807,
          39.1060,   39.1312,   39.1565,   39.1817,   39.2070,   39.2322,
          39.2575,   39.2827,   39.3080,   39.3332,   39.3585,   39.3585,
          39.3585,   39.3585,   39.3585,   39.3585,   39.3585,   39.3585,
          39.3585,   39.3585,   39.3585,   39.3585,   39.3585,   39.3585]
eqlats = np.array(eqlats)

# Read potential vorticity at 320-K isentropic surface
cubes = files.load('../iop5_36h.pp')
cubes.remove(cubes.extract('air_pressure')[0])
theta = convert.calc('air_potential_temperature', cubes)
pv = convert.calc('ertel_potential_vorticity', cubes)
pv.add_aux_coord(grid.make_coord(theta), [0, 1, 2])
pv320 = interpolate.to_level(pv, air_potential_temperature=[320])[0]
pv = pv320.data

lon, lat = cartography.get_xy_grids(pv320)
polelon = pv320.coord_system().grid_north_pole_longitude
polelat = pv320.coord_system().grid_north_pole_latitude
rlat, rlon = cartography.unrotate_pole(lon, lat, polelon, polelat)
phi = rlon
cos_phi = np.cos(phi)
nx, ny = pv.shape
x = np.arange(nx)
y = np.arange(ny)
iday = 0


# Find the contour of 2 PVU that wraps around the globe
cs = plt.contour(pv, [PV_tropo])
contours_fct = tropoc.get_contour_verts(cs)
tropopause_contour = tropoc.find_tropopause_contour(contours_fct[0])

if tropoc.is_closed_contour(tropopause_contour):
    path = Path(tropopause_contour)
    points = np.transpose(np.array([x.flatten(), y.flatten()]))
    inside = np.reshape(path.contains_points(points), pv.shape)

    # Ridge corresponds to points not inside the tropopause contour but with
    # latitudes higher than the equivalent latitude of the tropopause contour
    ridge = np.logical_and(np.logical_not(inside), phi > eqlats[iday])
    # Compute ridge area
    masked_cos_phi = np.ma.masked_where(np.logical_not(ridge), cos_phi)
    ridge_area = np.ma.sum(masked_cos_phi) * np.pi / 64800

else:
    print 'Open contour'
    ridge_area = -2

plt.close()
