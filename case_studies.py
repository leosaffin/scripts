"""Forecast objects for
"""
from datetime import datetime, timedelta
from mymodule.forecast import Forecast


def iop5():
    job_name = 'xjjhq'
    start_time = datetime(2011, 11, 28, 12)
    mapping = {start_time + timedelta(hours=lead_time):
               'datadir/' + job_name + '/' + job_name + 'a_' +
               str(lead_time).zfill(3) + '.pp'
               for lead_time in xrange(1, 37)}
    return Forecast(start_time, mapping)


def iop8():
    job_name = 'xjjhq'
    start_time = datetime(2011, 12, 7, 12)
    mapping = {start_time + timedelta(hours=lead_time):
               'datadir/' + job_name + '/' + job_name + '_p*' +
               str(lead_time).zfill(3)
               for lead_time in xrange(36)}

    return Forecast(start_time, mapping)
