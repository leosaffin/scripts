""" Create a forecast to load data
"""

import datetime
import cPickle as pickle
from mymodule import forecast

start_time = datetime.datetime(2011, 11, 28, 12)
dt = datetime.timedelta(hours=1)
directory = '/projects/diamet/lsaffi/xjjhq/xjjhqa_'
mapping = {start_time + n * dt: directory + str(n).zfill(3) + '.pp'
           for n in xrange(1, 37)}

iop5 = forecast.Forecast(start_time, mapping)
with open('/home/lsaffi/data/forecasts/iop5.pkl', 'w') as output:
    pickle.dump(iop5, output)
