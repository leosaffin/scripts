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


# DIAMET IOP5
start_time = datetime(2011, 11, 28, 12)
lead_times = [timedelta(hours=n) for n in range(1, 37)]

# Original IOP5 forecast with dynamics-tracer inconsistency including pressure
# solver increments
job_id = 'xjjhq'
filenames = ['xjjhqa_']
iop5 = generate_forecast(
    start_time, lead_times, job_id, filenames, suffix='.pp')


# Dynamics-tracer inconsistency using basic diagnostic without pressure solver
# increments
filenames = ['xjjhqb_', 'xjjhqb_nddiag_']
iop5b = generate_forecast(
    start_time, lead_times, job_id, filenames, suffix='.pp')


# Same as iop5b but using monotone limiter for PV tracer advection
job_id = 'iop5'
filenames = ['prognostics_', 'diagnostics_', 'pv_tracer_mono_']
iop5_mono = generate_forecast(start_time, lead_times, job_id, filenames)

# Theta tracers
filenames = ['prognostics_', 'diagnostics_', 'theta_tracers_']
iop5_theta = generate_forecast(start_time, lead_times, job_id, filenames)

# DIAMET IOP8
start_time = datetime(2011, 12, 7, 12)
lead_times = [timedelta(hours=n) for n in range(1, 37)]

# Dynamics-tracer inconsistency using basic diagnostic without pressure solver
# increments
job_id = 'xkcqa'
filenames = ['xkcqaa_*']

iop8 = generate_forecast(
    start_time, lead_times, job_id, filenames, suffix='.pp')
