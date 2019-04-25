"""
'datadir' and 'plotdir' hold the location of my data and plots which is different on different systems, so it is
modified here rather than in each script individually.
"""
import os

homepath = os.path.expanduser('~/Documents/meteorology/')
datadir = homepath + 'data/'
plotdir = homepath + 'output/'