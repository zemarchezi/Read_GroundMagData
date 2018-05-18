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


class ReadSupermag(object):
    """docstring for ReadSupermag."""
    def __init__(self, inidate='', enddate='', station='', filen = ''):
        # Initial time
        self.ini = inidate
        ###
        # End time
        self.end = enddate
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
        f = open(self.filename, 'r')

        self.data = f.readlines()
        f.close()


        self.stations = filter(lambda x: '-mlt' in x, self.data)[0].split('-mlt')

        # print(len(time))
        year = self.stations[1][17:21]
        Date = filter(lambda x: year+'\t' in x, self.data)
        self.time = []
        for d in Date:
            self.time.append(datetime.datetime(int(d[0:4]),int(d[5:7]),int(d[8:10]),int(d[11:13]),
                       int(d[14:16]),int(d[17:19]),int(d[20:22])))
        #
        #
        # #stations = (stations[0][-(len(stations)-95):-1]).split(',')
        self.stations = self.stations[1][49:-1].split(',')


    def readData(self):
        x, y, z = [], [], []
        for i in self.stations:
            temp_x, temp_y, temp_z = [], [], []
            d = filter(lambda x: i+'\t' in x, self.data)
            for k in d:
                temp_x.append(float(((k.split('\n')[0]).split('\t'))[1]))
                temp_y.append(float(((k.split('\n')[0]).split('\t'))[2]))
                temp_z.append(float(((k.split('\n')[0]).split('\t'))[3]))
            x.append(temp_x)
            y.append(temp_y)
            z.append(temp_z)

        self.north = pd.DataFrame(data=np.transpose(x), columns=self.stations, index=self.time)
        self.east = pd.DataFrame(data=np.transpose(y), columns=self.stations, index=self.time)
        self.down = pd.DataFrame(data=np.transpose(z), columns=self.stations, index=self.time)

        return (self.north, self.east , self.down)
