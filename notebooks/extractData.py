import os
import math
import h5py
import errno
import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import xml.etree.ElementTree as ETO
from scipy.interpolate import RectBivariateSpline

import plotly
from plotly.graph_objs import *
plotly.offline.init_notebook_mode()

import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

class extractData:
    """
    Class for extracting basin data from Badlands outputs.
    """

    def __init__(self, folder=None, ncpus=1):
        """
        Initialization function which takes the folder path to Badlands outputs
        and the number of CPUs used to run the simulation. It also takes the
        bounding box and discretization value at which one wants to interpolate
        the data.
        Parameters
        ----------
        variable : folder
            Folder path to Badlands outputs.
        variable: ncpus
            Number of CPUs used to run the simulation.
        """

        self.folder = folder
        if not os.path.isdir(folder):
            raise RuntimeError('The given folder cannot be found or the path is incomplete.')

        self.ncpus = ncpus
        self.x = None
        self.y = None
        self.z = None
        self.discharge = None
        self.cumchange = None

        return

    def loadHDF5(self, timestep=0):
        """
        Read the HDF5 file for a given time step.
        Parameters
        ----------
        variable : timestep
            Time step to load.
        """

        for i in range(0, self.ncpus):
            df = h5py.File('%s/tin.time%s.p%s.hdf5'%(self.folder, timestep, i), 'r')
            coords = np.array((df['/coords']))
            cumdiff = np.array((df['/cumdiff']))
            discharge = np.array((df['/discharge']))
            if i == 0:
                x, y, z = np.hsplit(coords, 3)
                c = cumdiff
                d = discharge
            else:
                c = np.append(c, cumdiff)
                d = np.append(d, discharge)
                x = np.append(x, coords[:,0])
                y = np.append(y, coords[:,1])
                z = np.append(z, coords[:,2])

        self.x = x
        self.y = y
        self.z = z
        self.discharge = d
        self.cumchange = c

        return