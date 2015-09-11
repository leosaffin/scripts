""" Holds information for loading archived files

This represents the interface between the files stored on mass and to postproc
and finally to RAM.
"""

import os
from mymodule.forecast import Forecast
from user_information import job_ids, letters, lead_times


path = '/projects/diamet/lsaffi/season/'


def download(time):
    """Downloads data for a single forecast from mass

    Args:
        time (datetime.datetime): The start time of the forecast. Maps to the
            filenames on mass and pp through the respective 'filename'
            functions

    Returns:
        Forecast : The requested forecast loaded onto the postprocessor
    """
    ID = job_ids[time]
    # Retrieve the .pp files from mass into the local directory
    for filename in mass_filenames(ID):
        os.system('moo get ' + filename + ' .')

    # Create a forecast object
    mapping = {}
    for lead_time in lead_times:
        mapping[time + lead_time] = \
            pp_filenames(lead_time, ID)

    return Forecast(time, mapping)


def clean_up(time):
    ID = job_ids[time]
    for lead_time in lead_times:
        for filename in pp_filenames(lead_time, ID):
            if 'analysis' not in filename:
                os.system('rm ' + filename)


# Functions mapping IDs to filenames
def mass_filenames(ID):
    return [':/crum/' + ID + '/' + 'ap' + letter + '.pp'
            for letter in letters]


def pp_filenames(lead_time, ID):
    lead_time = int(lead_time.total_seconds() / 3600)
    if lead_time == 0:
        return [path + ID + '.analysis.pp']
    else:
        return [ID + 'a_p' + letter + str(lead_time - 6).zfill(3) + '.pp'
                for letter in letters]
