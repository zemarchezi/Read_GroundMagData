from ReadSupermag import ReadSupermag
import datetime
import matplotlib.pyplot as plt

# inidate=datetime.datetime(2016,6,24,0,0), enddate=datetime.datetime(2016,6,28,0,0),

# rd = ReadCarisma(inidate=datetime.datetime(2014,03,25,00,00), enddate=datetime.datetime(2014,03,25,23,59))
rd = ReadSupermag(filen = '20180518-19-53-supermag.csv')

rd.directories(downlDir='/home/jose/MEGA/Doutorado/Progs/read_SuperMag/dados/', plotDir='/home/jose/MEGA/Doutorado/Progs/read_SuperMag/plots/')

rd.files()

rd.readInfo()

x = rd.readData()

print(x[1])

# x[1].plot(sharex=True, subplots=True)
# plt.show()
