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
    def __init__(self, inidate='', enddate='', station=''):
        # Initial time
        self.ini = inidate
        ###
        # End time
        self.end = enddate
        self.station = station


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
        filen = '%04d-%02d-%02d*%04d-%02d-%02d*/%04d%02d%02d*%s*' %(self.ini.year, self.ini.month,
                                                  self.ini.day,self.end.year, self.end.month,self.end.day,
                                                  self.ini.year,self.ini.month,self.ini.day,
                                                  self.station)
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



class ReadSupermag(object):
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
        if self.filen.split('.')[1] == 'txt':
            f = open(self.filename, 'r')
            self.data = f.readlines()
            f.close()
            self.stations = list(filter(lambda x: '-mlt' in x, self.data))[0].split('-mlt')

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

        if self.filen.split('.')[1] == 'csv':
            self.data = pd.read_csv(self.filename, index_col=0)
            self.data.index = pd.to_datetime(self.data.index)
            stat = self.data['IAGA'][self.data.index==self.data.index[0]]
            self.stations = []
            for i in range(0,len(stat)):
                self.stations.append(stat[i])

            self.time = self.data.IAGA[self.data.IAGA == self.stations[0]].index

    def readData(self):
        if self.filen.split('.')[1] == 'txt':
            x, y, z = [], [], []
            for i in self.stations:
                temp_x, temp_y, temp_z = [], [], []
                d = list(filter(lambda x: i+'\t' in x, self.data))
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

            return ([self.north, self.east , self.down, self.station])

        if self.filen.split('.')[1] == 'csv':
            temp_x, temp_y, temp_z = [], [], []
            for i in self.stations:
                temp_x.append(self.data[self.data.IAGA == i]['N'])
                temp_y.append(self.data[self.data.IAGA == i]['E'])
                temp_z.append(self.data[self.data.IAGA == i]['Z'])

            self.north = pd.DataFrame(data=np.transpose(temp_x), columns=self.stations, index=self.time)
            self.east = pd.DataFrame(data=np.transpose(temp_y), columns=self.stations, index=self.time)
            self.down = pd.DataFrame(data=np.transpose(temp_z), columns=self.stations, index=self.time)

            return ([self.north, self.east, self.down])



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

        fil = open(self.filename, 'r') # open the file
        data = fil.readlines()  # read the lines
        lat = data[4][24:30] # load latitude and longitude
        lon = data[5][24:30]
        sk = len(data) - 1441 # set how many lines of headers to skip
        fil.close()

        self.data = pd.read_csv(self.filename, skiprows=sk, delim_whitespace=True, index_col=[0,1])

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
