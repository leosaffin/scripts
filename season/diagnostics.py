class Suite():
    """A collection of diagnostics used to analyse a forecast
    """

    def __init__(self, forecast):
        self.forecast = forecast

    def set_time(self, time):
        self.forecast.set_time(time)

    def analyse(self):
        pass

    def save(self):
        pass

    def __del__(self):
        print('Analysed ' + str(self.forecast.start_time))


class Diagnostic():
    """Base class for individual diagnostics
    """

dipole = Diagnostic()
