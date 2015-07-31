#!/usr/bin/env python2.7
"""Analysis of a season of forecasts
"""

import datetime
import archive
from diagnostics import Suite
from user_information import job_ids


def main(start_time, end_time, dt):
    time = start_time
    suites = []
    while time <= end_time:
        if time in job_ids:
            # Load the files from mass to postproc and into a forecast
            new_forecast = archive.download(time)
            suites.append(Suite(new_forecast, job_ids[time]))
        for suite in suites:
            update_time(suite, time)

        time += dt


def update_time(suite, time):
    try:
        suite.set_time(time)
        suite.analyse()
    except KeyError:
        # Remove the suite if it has exceeded the time
        suite.save()
        archive.clean_up(suite.forecast.start_time)
        del suite


if __name__ == '__main__':
    start_time = datetime.datetime(2013, 11, 1)
    end_time = datetime.datetime(2014, 2, 3)
    dt = datetime.timedelta(hours=6)
    main(start_time, end_time, dt)
