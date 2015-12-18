#!/usr/bin/env python2.7
"""Analysis of a season of forecasts
"""

import cProfile as profile
import datetime
from itertools import combinations
import archive
from diagnostics import Suite
from user_information import job_ids


def main(start_time, end_time, dt):
    time = start_time
    suites = []
    # Loop until the end of the final forecast
    while time <= end_time:
        print time
        if time in job_ids:
            # Load the files from mass to postproc and into a forecast
            new_forecast = archive.download(time)
            # Associate this forecast with an analysis suite
            suite = Suite(new_forecast, job_ids[time])
            # Set the suite time to its start time to trigger loading
            suite.set_time(time)
            # Add the suite to the list of suites being analysed
            suites.append(suite)

        # Compare different forecasts
        # itertools.combinations gives all unique pairs
        for suite_pair in combinations(suites, 2):
            compare(*suite_pair)
        print('Compared Forecasts')

        # Update reference time and trigger analysis of timestep
        time += dt
        # Use a list comprehension so suites exceeding times can be removed
        # within the loop
        suites = [suite for suite in suites if update_time(suite, time)]
        print('Analysed Forecasts')


def update_time(suite, time):
    """Updates the suite time and triggers an analysis of that timestep

    Returns:
        True/False: Tells us whether the time has exceeded the suite bounds and
            should be kept (True = Keep, False = Delete)
    """
    try:
        suite.set_time(time)
        suite.analyse()
        return True

    except KeyError:
        # Save the data from the suite
        suite.save()
        archive.clean_up(suite.forecast.start_time)
        return False


def compare(suite1, suite2):
    """
    """
    if suite1.forecast.start_time < suite2.forecast.start_time:
        suite1.analyse_errors(suite2)
    else:
        suite2.analyse_errors(suite1)


if __name__ == '__main__':
    start_time = datetime.datetime(2013, 11, 1)
    end_time = datetime.datetime(2014, 2, 4)
    dt = datetime.timedelta(hours=6)
    profile.run('main(start_time, end_time, dt)',
                '/home/lsaffi/data/season/profile')
