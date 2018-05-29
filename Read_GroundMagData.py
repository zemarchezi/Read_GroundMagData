# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
"""
Created on May  018
@author: zemarchezi
"""
import numpy as np
import datetime
import os
import glob
import pandas  as pd
import sys
sys.path.insert(0, '/home/jose/MEGA/Doutorado/Progs/SignalAnalysis')
from analysisFunc import geo2mag

__author__ = 'zemarchezi'

class ReadCarisma():
    """docstring for ReadGrBasedData."""
    def __init__(self, inidate='', enddate=''):
        # Initial time
        self.ini = inidate
        ###
        # End time
        self.end = enddate
        # self.station = station


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
        self.day_arr = [self.ini + datetime.timedelta(days=x) for x in range(0, int(str(self.end-self.ini)[0])+1)]
        self.files = []
        for i in self.day_arr:
            filen = '**/*%04d%02d%02d*' %(i.year, i.month, i.day)
            self.filename = self.dataDownlDir + filen
            print(self.filename)
            self.files.extend(glob.glob(self.filename))

        self.files.sort()

    def readData(self):
        ######
        ## Abre os arquivos e extrai as componentes
        #
        latitude, lshell = [], []
        x, y, z, h, mh, t, stations = [], [], [], [], [], [], []
        for i in self.files:
            print(i)
            f = open(i, 'r')
            ss = f.readline().split(' ') ## Open the file and read the first line
            f.close()
            ######
            ## Open and read the x, y, and z compoents
            #
            try:
                temp_t, temp_x, temp_y, temp_z = np.loadtxt(i, skiprows=1, usecols=(0,1,2,3), unpack=True)
                temp_h = np.sqrt(temp_x**2 + temp_y**2 + temp_z**2) # Calculate the H component
                temp_mh = temp_h - (np.mean(temp_h)) # Subtract the mean value of the field
                #####
                ## Create an time array from the data
                time = []
                t_sec = []
                for i in temp_t:
                    ## Datetime formaat
                    time.append(datetime.datetime(int(str(int(i))[0:4]), int(str(int(i))[4:6]),
                                                  int(str(int(i))[6:8]), int(str(int(i))[8:10]),
                                                  int(str(int(i))[10:12]), int(str(int(i))[12:14])))
                    ## Second dta array
                    t_sec.append(int(str(int(i))[8:10])*3600 + int(str(int(i))[10:12])*60 + int(str(int(i))[12:14]))

                station = [ss[0]]*len(time) # Create an list with the stations names
                lat = [ss[2]]* len(time) # Create a list with the corresponding latitudes
                magc = geo2mag([float(ss[2]), float(ss[3])])
                l = [(np.sin(np.deg2rad(90-float(magc[0])))) ** (-2)] * len(time) # McIlwain parameter


                ## Create an list with the components for each station
                t.extend(time) # time array
                x.extend(temp_x) # x component
                y.extend(temp_y) # y component
                z.extend(temp_z) # z component
                h.extend(temp_h) # H component
                mh.extend(temp_mh) # mean variation of H component
                stations.extend(station)
                latitude.extend(lat)
                lshell.extend(l)
            except (Exception) as e:
                print (e)


        dd = pd.DataFrame(np.transpose([x,y,z,h,mh]), index=t,columns=['x', 'y', 'z', 'h', 'mean_h'])
        dd['stat'] = stations
        dd['lat'] = latitude
        dd['lshell'] = lshell
        self.dd = dd.drop_duplicates()
#            dat.append(dd.to_dict())
        return (self.dd)


    def separateStat(self):
        stat = []
        llat = []
        lsh = []
        for i in self.day_arr:
            stat.append(set(self.dd['stat'][self.dd.index==i]))
            llat.append(set(self.dd['lat'][self.dd.index==i]))
            lsh.append(set(self.dd['lshell'][self.dd.index==i]))

        self.eqStat = list(set.intersection(*stat))
        self.eqlat = list(set.intersection(*llat))
        self.eqlshell = list(set.intersection(*lsh))

        ######
        ## Sort the stations according to the latitudes, from higher to lower
        #
        stat = dict(zip(self.eqStat, self.eqlat))
        print (stat)
        shell = dict(zip(self.eqStat, self.eqlshell))
        print shell
        self.eqStat.sort(key=stat.get, reverse=True)

        xAllStat = pd.DataFrame()
        yAllStat = pd.DataFrame()
        zAllStat = pd.DataFrame()
        hAllStat = pd.DataFrame()
        mhAllStat = pd.DataFrame()
        for i in self.eqStat:
            xAllStat[i] = self.dd[self.dd['stat']==i]['x']
            yAllStat[i] = self.dd[self.dd['stat']==i]['y']
            zAllStat[i] = self.dd[self.dd['stat']==i]['z']
            hAllStat[i] = self.dd[self.dd['stat']==i]['h']
            mhAllStat[i]= self.dd[self.dd['stat']==i]['mean_h']

        return ([xAllStat,yAllStat,zAllStat,hAllStat,mhAllStat, self.eqlat])


####################################################################################
#  Supermag
####################################################################################
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
