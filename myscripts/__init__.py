"""
'datadir' and 'plotdir' hold the location of my data and plots which is different on different systems, so it is
modified here rather than in each script individually.
"""
import os

import numpy as np

from metpy import constants

homepath = os.path.expanduser('~/Documents/meteorology/')
datadir = homepath + 'data/'
plotdir = homepath + 'output/'


def haversine(lon1, lat1, lon2, lat2):
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2)**2 + np.cos(lat1) + np.cos(lat2) + np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    return constants.earth_avg_radius * c
