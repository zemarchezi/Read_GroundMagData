# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
"""
Created onmain. May  8, 2018

@author: zemarchezi
"""
import numpy as np
import matplotlib.pylab as plt
import datetime
import os, re, ssl, urllib, sys, fnmatch
import glob
import pandas  as pd
from collections import OrderedDict

__author__ = 'zemarchezi'


class ReadIntermagnet(object):
    """docstring for ReadSupermag."""
    def __init__(self, station='', filen = ''):
        # Initial time
        # self.ini = inidate
        ###
        # End time
        # self.end = enddate
        self.station = station
        self.filen = filen

    def directories(self, downlDir, plotDir):
        ####
        # Paths
        # self.path = os.getcwd() #'/home/jose/MEGA/Doutorado/Progs/plot_ULF/dados/'
        # if not os.path.exists(self.path + '/'+DownlDir+'/'):
        if not os.path.exists(downlDir):
            os.makedirs(downlDir)
        if not os.path.exists(plotDir):
            os.makedirs(plotDir)

        self.dataDownlDir = downlDir
        self.plotDir = plotDir

    def files(self):
        self.filename = self.dataDownlDir + self.filen
        self.files = glob.glob(self.filename)
        self.files.sort()

    def readInfo(self):

        self.data = pd.read_csv(self.filename, skiprows=20, delim_whitespace=True, index_col=[0,1])

        self.time = list(self.data.index)

        for i in range(0,len(self.time)):
            self.time[i] = pd.to_datetime(' '.join(map(str,self.time[i])))

        self.data.index = self.time

        tempstat = self.data.columns[1:]

        return ([self.data])

    def readData(self):
        for s in self.stations:
            filen = s + '*'
            local_file = dataDownlDir + filen
            files_mag = glob.glob(local_file) # list the files
            files_mag.sort() # sort
            for f in files_mag:
                print ('opening -> ' + f[-19:])
                fil = open(f, 'r') # open the file
                data = fil.readlines()  # read the lines
                lat = data[4][24:30] # load latitude and longitude
                lon = data[5][24:30]
                sk = len(data) - 1440 # set how many lines of headers to skip
                fil.close()
                print ('loading the geomagnetic components...')
                # load the X, Y and Z components
                X, Y, Z = np.loadtxt(f, skiprows=sk, usecols=(3, 4, 5), unpack = True)
                # locate and replace gaps
                X[X == 99999.00] = 'nan'
                Y[Y == 99999.00] = 'nan'
                Z[Z == 99999.00] = 'nan'
                H = np.sqrt(X ** 2 + Y ** 2) # Calculate the H component
                Hn = []
                for i in range(0, 1440):
                    Hn.append(H[i] - H[0]) # Extract the local background
                os.remove(f) # remove the file
