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

class ReadCarisma():
    """docstring for ReadGrBasedData."""
    def __init__(self, inidate='', enddate=''):
        # Initial time
        self.ini = inidate
        ###
        # End time
        self.end = enddate


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
        ####
        ## Define o diretório e nome dos arquivos que serão abertos
        #
        filen = '%04d-%02d-%02d*%04d-%02d-%02d*/%04d%02d%02d*' %(self.ini.year, self.ini.month,
                                                  self.ini.day,self.end.year, self.end.month,self.end.day,
                                                  self.ini.year,self.ini.month,self.ini.day)
        self.filename = self.dataDownlDir + filen
        print(self.filename)
        self.files = glob.glob(self.filename)
        print(self.files)
        self.files.sort()

    def readData(self):
        ######
        ## Abre os arquivos e extrai as componentes
        #
        stations, lat = [], []
        x, y, z, h, t, mh = [], [], [], [], [], []
        for i in self.files:
            print(i)
            f = open(i, 'r')
            ss = f.readline().split(' ') ## Open the file and read the first line
            f.close()
            stations.append(ss[0]) # Create an list with the stations names
            lat.append(ss[2]) # Create a list with the corresponding latitudes
            ######
            ## Open and read the x, y, and z compoents
            #
            temp_t, temp_x, temp_y, temp_z = np.loadtxt(i, skiprows=1, usecols=(0,1,2,3), unpack=True)
            temp_h = np.sqrt(temp_x**2 + temp_y**2 + temp_z**2) # Calculate the H component
            temp_mh = temp_h - (np.mean(temp_h)) # Subtract the mean value of the field
            #####
            ## Create an list with the components for each station
            t.append(temp_t) # time array
            x.append(temp_x) # x component
            y.append(temp_y) # y component
            z.append(temp_z) # z component
            h.append(temp_h) # H component
            mh.append(temp_mh) # mean variation of H component
        #####
        ## Create an time array from the data
        time = []
        t_sec = []
        for i in t[0]:
            ## Datetime formaat
            time.append(datetime.datetime(int(str(int(i))[0:4]), int(str(int(i))[4:6]),
                                          int(str(int(i))[6:8]), int(str(int(i))[8:10]),
                                          int(str(int(i))[10:12]), int(str(int(i))[12:14])))
            ## Second dta array
            t_sec.append(int(str(int(i))[8:10])*3600 + int(str(int(i))[10:12])*60 + int(str(int(i))[12:14]))

        ######
        ## Create an table formatation for the components and filtered data
        #
        tab_x = pd.DataFrame(data=np.transpose(x), columns=stations, index=time)
        tab_y = pd.DataFrame(data=np.transpose(y), columns=stations, index=time)
        tab_z = pd.DataFrame(data=np.transpose(z), columns=stations, index=time)
        tab_h = pd.DataFrame(data=np.transpose(mh), columns=stations, index=time)
        ######
        ## Sort the stations according to the latitudes, from higher to lower
        #
        stat = dict(zip(stations, lat))
        stations.sort(key=stat.get, reverse=True)

        sa = []
        for i in stations:
            sa.append(i+ ' ' +stat[i]+'$^{\circ}$')

        newname = dict(zip(stations, sa))

        ######
        ## Order the Keys of the components and filtered data DataFrames
        temp_x = OrderedDict.fromkeys(stations)
        temp_y = OrderedDict.fromkeys(stations)
        temp_z = OrderedDict.fromkeys(stations)
        temp_h = OrderedDict.fromkeys(stations)
        ######
        ## Order the position of the coluns in the Data Frames
        #
        for i in stations:
            temp_x[i] = tab_x[i]
            temp_y[i] = tab_y[i]
            temp_z[i] = tab_z[i]
            temp_h[i] = tab_h[i]
        #####
        ## Crete the definitive Data Frame for the data
        #
        x = pd.DataFrame(temp_x)
        y = pd.DataFrame(temp_y)
        z = pd.DataFrame(temp_z)
        h = pd.DataFrame(temp_h)
        x = x.rename(columns=newname)
        y = y.rename(columns=newname)
        z = z.rename(columns=newname)
        h = h.rename(columns=newname)

        return ([x, y, z, h])
