#!/usr/bin/env python2.7
"""Analysis of a season of forecasts
"""

import cProfile as profile
import datetime
import archive
from diagnostics import Suite
from user_information import job_ids


def main(start_time, end_time, dt):
    time = start_time
    suites = []
    while time <= end_time:
        print time
        if time in job_ids:
            # Load the files from mass to postproc and into a forecast
            new_forecast = archive.download(time)
            suite = Suite(new_forecast, job_ids[time])
            suite.set_time(time)
            suites.append(suite)
        # Compare different forecasts
        for n in xrange(len(suites) - 1):
            compare(suites[n], suites[n + 1])
        print('Compared Forecasts')
        time += dt
        for suite in suites:
            update_time(suite, time, suites)
        print('Analysed Forecasts')


def update_time(suite, time, suites):
    try:
        suite.set_time(time)
        suite.analyse()
    except KeyError:
        # Remove the suite if it has exceeded the time
        suite.save()
        archive.clean_up(suite.forecast.start_time)
        suites.remove(suite)
        del suite


def compare(suite1, suite2):
    """
    """
    if suite1.forecast.start_time < suite2.forecast.start_time:
        suite1.analyse_errors(suite2)
    else:
        suite2.analyse_errors(suite1)


if __name__ == '__main__':
    start_time = datetime.datetime(2013, 11, 30)
    end_time = datetime.datetime(2014, 2, 4)
    dt = datetime.timedelta(hours=6)
    profile.run('main(start_time, end_time, dt)',
                '/home/lsaffi/data/season/profile')
