"""Generate forecast objects for case studies
"""
from datetime import datetime, timedelta
from mymodule.forecast import Forecast
from mymodule.user_variables import datadir


def generate_forecast(start_time, lead_times, job_id, filenames, suffix='.nc'):
    mapping = {}
    for n, dt in enumerate(lead_times, start=1):
        mapping[start_time + dt] = make_filenames(job_id, filenames, n, suffix)

    return Forecast(start_time, mapping)


def generate_analyses(start_time, dt, nt):
    dt = timedelta(hours=dt)
    mapping = {}
    for n in range(nt):
        time = start_time + n * dt
        mapping[time] = (datadir + job_id + '/' +
                         str(time)[0:10].replace('-', '') +
                         '_analysis' + str(time)[11:13] + '.nc')

    return Forecast(start_time, mapping)


def make_filenames(job_id, filenames, n, suffix):
    names = []
    for filename in filenames:
        names.append(datadir + job_id + '/' +
                     filename + str(n).zfill(3) + suffix)

    return names


def generate_season_forecast(YYYY, MM, DD):
    start_time = datetime(YYYY, MM, DD)
    lead_times = range(0, 61, 6)
    mapping = {start_time + timedelta(hours=dt):
               datadir + '/season/' + str(start_time)[0:10].replace('-', '') +
               '_T+' + str(dt).zfill(2) + '.nc'
               for dt in lead_times}

    return Forecast(start_time, mapping)


# DIAMET IOP5
start_time = datetime(2011, 11, 28, 12)
lead_times = [timedelta(hours=n) for n in range(1, 37)]

# Original IOP5 forecast with dynamics-tracer inconsistency including pressure
# solver increments
job_id = 'xjjhq'
filenames = ['xjjhqa_']
iop5 = generate_forecast(
    start_time, lead_times, job_id, filenames, suffix='.pp')


job_id = 'iop5'
# Dynamics-tracer inconsistency using basic diagnostic without pressure solver
# increments
filenames = ['prognostics_', 'diagnostics_', 'pv_tracers_']
iop5b = generate_forecast(start_time, lead_times, job_id, filenames)

# Same as iop5b but using monotone limiter for PV tracer advection
filenames = ['prognostics_', 'diagnostics_', 'pv_tracer_mono_']
iop5_mono = generate_forecast(start_time, lead_times, job_id, filenames)

# Theta tracers
filenames = ['prognostics_', 'diagnostics_', 'theta_tracers_']
iop5_theta = generate_forecast(start_time, lead_times, job_id, filenames)

# Analyses
iop5_analyses = generate_analyses(start_time, 6, 7)

# IOP5 with start time 12-hours earlier
job_id = 'iop5_early'
start_time = datetime(2011, 11, 28)
lead_times = [timedelta(hours=n) for n in range(1, 49)]
filenames = ['prognostics_', 'diagnostics_', 'pv_tracers_']
iop5_early = generate_forecast(start_time, lead_times, job_id, filenames)

# IOP5 early start time with extended domain
job_id = 'iop5_extended'
iop5_extended = generate_forecast(start_time, lead_times, job_id, filenames)

# IOP5 global
job_id = 'iop5_global'
iop5_global = generate_forecast(start_time, lead_times, job_id, filenames)

# DIAMET IOP8
job_id = 'iop8'
filenames = ['prognostics_', 'diagnostics_', 'pv_tracers_', 'theta_tracers_']
start_time = datetime(2011, 12, 7, 12)
lead_times = [timedelta(hours=n) for n in range(1, 37)]

# Dynamics-tracer inconsistency using basic diagnostic without pressure solver
# increments
iop8 = generate_forecast(start_time, lead_times, job_id, filenames)
iop8_analyses = generate_analyses(start_time, 6, 7)

# IOP8 with long-wave radiation increments set to zero
job_id = 'iop8_no_lw'
iop8_no_lw = generate_forecast(start_time, lead_times, job_id, filenames)

# IOP8 with latent heat set to small numbers
job_id = 'iop8_no_microphysics'
iop8_no_lw = generate_forecast(start_time, lead_times, job_id, filenames)
