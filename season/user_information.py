"""Define variables specific to the run
"""

import datetime
from string import ascii_lowercase

# The start/end cftime of the runs period and the increment between start dumps
first_start_time = datetime.datetime(2013, 11, 1)
last_start_time = datetime.datetime(2014, 1, 31)
dt = datetime.timedelta(days=1)

time = first_start_time
start_times = []
while time <= last_start_time:
    start_times.append(time)
    time += dt

# A list of the lead times output for each forecast
lead_times = [datetime.timedelta(hours=n) for n in xrange(0, 61, 6)]

# A list of reserved ids for the job identifiers
identifiers = ['xlib', 'xlic', 'xlid', 'xlie']
reserved_ids = [identifier + letter for identifier in identifiers
                for letter in ascii_lowercase]
# Re order reserved IDs into time order
reserved_ids = reserved_ids[66:96] + reserved_ids[0:62]

# Dictionary mapping start cftime to job ID
job_ids = {time: ID for time, ID in zip(start_times, reserved_ids)}

# Letters used in forecast .pp files
letters = ['a', 'b', 'c', 'd']


# A dictionary mapping of filenames to list of functions to modify them
def EXPT_ID(job):
    return'EXPT_ID=\'' + job.expt_ID()


def JOB_ID(job):
    return'JOB_ID=\'' + job.job_ID()


def EXPTID(job):
    return'EXPTID=' + job.expt_ID()


def JOBID(job):
    return'JOBID=' + job.job_ID()


def FULL_ID(job):
    return job.ID()


def DATE(job):
    return job.datestr()


def MODEL_BASIS_TIME(job):
    time = job.time
    string = ('MODEL_BASIS_TIME= ' +
              str(time.year) + ' , ' +
              str(time.month) + ' , ' +
              str(time.day) + ' , ' +
              str(time.hour) + ' , ' +
              str(time.minute) + ' , ' +
              str(time.second))
    return string

files = {}
files['CNTLALL'] = [EXPT_ID, JOB_ID, MODEL_BASIS_TIME]
files['CONTCNTL'] = [EXPT_ID, JOB_ID, MODEL_BASIS_TIME]
files['INITHIS'] = [FULL_ID, DATE]
files['SCRIPT'] = [EXPTID, JOBID]
files['SUBMIT'] = [FULL_ID]
files['umuisubmit_run'] = [FULL_ID, EXPTID, JOBID]


# The job to base other jobs on
base_start_time = datetime.datetime(2013, 12, 1)
base_directory = '/home/lsaffi/umui_runs/xkjjd-106095443'
