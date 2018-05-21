from ReadIntermagnet import ReadIntermagnet
import datetime
import matplotlib.pyplot as plt
from DataDownloader import DataDownloader
import os, re, ssl, urllib, sys, fnmatch
# inidate=datetime.datetime(2016,6,24,0,0), enddate=datetime.datetime(2016,6,28,0,0),

station = 'fcc'
year = '2016'
month = '05'
days = ['23']
host = 'ftp.intermagnet.org' # ftp host name
user = 'imaginpe' # ftp user name
password = 'd@a^DGE' # ftp password
# Directory contain the data
working_directory = 'minute/variation/IAGA2002/'+year+'/'+month+'/'

dataDownlDir = '/home/jose/MEGA/Doutorado/Progs/read_plotSpec_Intermag/dados/data20180521125025/'

listFilename = []
for d in days:
    listFilename.append(station+year+month+d+'vmin.min')

print (listFilename)

# filename = station+year+month+day+'vmin.min' # data filename

# Creating a instance of MarxDownloader
mx = DataDownloader(host, user, password)

mx.set_user_and_password(user, password)


# Connecting
mx.connectFTP()

mx.set_output_directory(dataDownlDir)

mx.set_directoryFTP(working_directory)

mx.download_one_dataFTP(listFilename[0])




# rd = ReadCarisma(inidate=datetime.datetime(2014,03,25,00,00), enddate=datetime.datetime(2014,03,25,23,59))
rd = ReadIntermagnet(filen = listFilename[0])

rd.directories(downlDir='/home/jose/MEGA/Doutorado/Progs/read_plotSpec_Intermag/dados/data20180521125025/', plotDir='/home/jose/MEGA/Doutorado/Progs/read_SuperMag/plots/')

rd.files()

x = rd.readInfo()

# x = rd.readData()

print(x[0])

# x[1].plot(sharex=True, subplots=True)
# plt.show()
