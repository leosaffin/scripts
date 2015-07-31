import numpy as np


# Constant parameters for each forecast
bins = np.linspace(0, 8, 33)


class Suite():
    """A collection of diagnostics used to analyse a forecast
    """

    def __init__(self, forecast, id):
        self.forecast = forecast
        self.id = id

    def set_time(self, time):
        self.forecast.set_time(time)

    def analyse(self):
        # Extract the cubes at the current time
        cubes = self.forecast.cubelist

        # Make a mask

        # Calculate the tropopause dipole
        dipole = diagnostic.averaged_over(variables, bins, adv.data,
                                              mass, mask=mask)

    def save(self):
        pass

    def __del__(self):
        print('Analysed ' + str(self.forecast.start_time))


class Diagnostic():
    """Base class for individual diagnostics
    """
