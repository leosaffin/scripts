import iris

from pylagranto import trajectory

from myscripts.projects import plotdir
from myscripts import datadir

plotdir = plotdir + 'nawdex/wcb_airmass/'
datadir = datadir + "nawdex/"


class NAWDEXCaseStudy:

    def __init__(self, name, storm_name, forecast_start):
        self.name = name
        self.storm_name = storm_name
        self.forecast_start = forecast_start
        return

    @property
    def forecast_filename(self):
        return datadir + "um-forecasts/{}.nc".format(self.name)

    @property
    def isentropic_trajectory_filename(self):
        return (datadir + "trajectories/{}/{}_TrajectoryEnsemble_backward.pkl").format(
            self.name, self.forecast_start)

    @property
    def lagrangian_trajectory_filename(self):
        return (datadir + "trajectories/{}/{}_TrajectoryEnsemble_new.pkl").format(
            self.name, self.forecast_start)

    def load_forecast(self):
        return iris.load(self.forecast_filename)

    def load_trajectories(self, method="isentropic"):
        if method.lower() == "isentropic":
            return trajectory.load(self.isentropic_trajectory_filename)
        elif method.lower() == "lagrangian":
            return trajectory.load(self.lagrangian_trajectory_filename)
        else:
            raise KeyError("Only isentropic and lagrangian trajectories available")


case_studies = dict(
    IOP3=NAWDEXCaseStudy("IOP3", "Vladiana", "20160922_12"),
    IOP5=NAWDEXCaseStudy("IOP5", "Walpurga", "20160926_12"),
    IOP6=NAWDEXCaseStudy("IOP6", "Stalactite Cyclone", "20160930_12"),
    IOP7=NAWDEXCaseStudy("IOP7", "Frontal-Wave Cyclone", "20161003_12"),
)
