# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
from Read_GroundMagData import ReadCarisma
import datetime
import matplotlib.pyplot as plt
from DataDownloader import DataDownloader
import os, re, ssl, urllib, sys, fnmatch

dataDownlDir = '/home/jose/Documents/carisma_data/'
plotDir = '/home/jose/Documents/dados/plots/'



rd = ReadCarisma(inidate=datetime.datetime(2016,7,19), enddate=datetime.datetime(2016,7,20))

rd.directories(downlDir=dataDownlDir, plotDir=plotDir)

rd.files()

dat2 = rd.readData()

ss = rd.separateStat()

print (ss[5])

ss[4].plot(sharex=True, subplots=True)
plt.show()

# inidate=datetime.datetime(2016,6,24,0,0), enddate=datetime.datetime(2016,6,28,0,0),
#
# station = 'kou'
# year = '2015'
# month = '05'
# days = ['23']
# host = 'ftp.intermagnet.org' # ftp host name
# user = 'imaginpe' # ftp user name
# password = 'd@a^DGE' # ftp password
# # Directory contain the data
# working_directory = 'minute/variation/IAGA2002/'+year+'/'+month+'/'
#
# dataDownlDir = '/home/jose/MEGA/Doutorado/Progs/read_plotSpec_Intermag/dados/data20180521125025/'
#
# listFilename = []
# for d in days:
#     listFilename.append(station+year+month+d+'vmin.min')
#
# print (listFilename)
#
# # filename = station+year+month+day+'vmin.min' # data filename
#
# # Creating a instance of MarxDownloader
# mx = DataDownloader(host, user, password)
#
# mx.set_user_and_password(user, password)
#
#
# # Connecting
# mx.connectFTP()
#
# mx.set_output_directory(dataDownlDir)
#
# mx.set_directoryFTP(working_directory)
#
# mx.download_one_dataFTP(listFilename[0])
#
#
#
#
# # rd = ReadCarisma(inidate=datetime.datetime(2014,03,25,00,00), enddate=datetime.datetime(2014,03,25,23,59))
# rd = ReadIntermagnet(filen = listFilename[0])
#
# rd.directories(downlDir='/home/jose/MEGA/Doutorado/Progs/read_plotSpec_Intermag/dados/data20180521125025/', plotDir='/home/jose/MEGA/Doutorado/Progs/read_SuperMag/plots/')
#
# rd.files()
#
# x = rd.readInfo()
#
# # x = rd.readData()
#
# x[0].plot(sharex=True, subplots=True, y=['KOUX', 'KOUY', 'KOUZ'])
# plt.show()
