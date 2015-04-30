"""
"""

import os
import glob
import datetime


def basis_time_command(new_time, old_time, filename):
    return ('sed \'s/' + time_str(old_time) + time_str(new_time) +
            ' < ' + filename + ' > ' + filename + '_NEW')


def time_str(time):
    return (str(time.year) + ' , ' + str(time.month) + ' , ' +
            str(time.day) + '/')

start_time = datetime.date(2013, 12, 1)
dt = datetime.timedelta(days=1)

# Replace JOB ID in all files
for uri in glob.glob('*'):
    pass
# Change start dump in INITHIS

# Change basis time in CNTALL and CONTCNTL
old_time = start_time
os.system(basis_time_command(start_time, old_time, 'CNTLALL'))
os.system('mv CNTLALL_NEW CNTLALL')
os.system(basis_time_command(start_time, old_time, 'CONTCNTL'))
os.system('mv CONCNTL_NEW CONTCNTL')

# Execute UMSUBMIT
#os.system('UMSUBMIT -h ' + host + '-u lsaffi' + job_id)
