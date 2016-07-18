"""Forecast objects for
"""
from datetime import datetime, timedelta
from mymodule.forecast import Forecast


def generate_forecast(start_time, lead_times, job_id, filenames, suffix='.nc'):
    mapping = {}
    for n, dt in enumerate(lead_times, start=1):
        mapping[start_time + dt] = make_filenames(job_id, filenames, n, suffix)

    return Forecast(start_time, mapping)


def make_filenames(job_id, filenames, n, suffix):
    names = []
    for filename in filenames:
        names.append('datadir/' + job_id + '/' +
                     filename + str(n).zfill(3) + suffix)

    return names


# Original IOP5 forecast with dynamics-tracer inconsistency including pressure
# solver increments
def iop5():
    start_time = datetime(2011, 11, 28, 12)
    lead_times = [timedelta(hours=n) for n in range(1, 37)]
    job_id = 'xjjhq'
    filenames = ['xjjhqa_']

    return generate_forecast(start_time, lead_times, job_id,
                             filenames, suffix='.pp')


# Dynamics-tracer inconsistency using basic diagnostic without pressure solver
# increments
def iop5b():
    start_time = datetime(2011, 11, 28, 12)
    lead_times = [timedelta(hours=n) for n in range(1, 37)]
    job_id = 'xjjhq'
    filenames = ['xjjhqb_', 'xjjhqb_nddiag_']

    return generate_forecast(start_time, lead_times, job_id,
                             filenames, suffix='.pp')


# Same as iop5b but using monotone limiter for PV tracer advection
def iop5_mono():
    start_time = datetime(2011, 11, 28, 12)
    lead_times = [timedelta(hours=n) for n in range(1, 37)]
    job_id = 'iop5'
    filenames = ['prognostics_', 'diagnostics_', 'pv_tracer_mono_']

    return generate_forecast(start_time, lead_times, job_id, filenames)


def iop8():
    start_time = datetime(2011, 12, 7, 12)
    lead_times = [timedelta(hours=n) for n in range(1, 37)]
    job_id = 'xkcqa'
    filenames = ['xkcqaa_*']

    return generate_forecast(start_time, lead_times, job_id,
                             filenames, suffix='.pp')
