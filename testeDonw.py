from ReadGroundBasedData import ReadCarisma
import datetime
import matplotlib.pyplot as plt

rd = ReadCarisma(inidate=datetime.datetime(2014,03,25,00,00), enddate=datetime.datetime(2014,03,25,23,59))

rd.directories(downlDir='/home/jose/Documents/carisma_data/', plotDir='/home/jose/MEGA/Doutorado/Progs/Read_GroundMagData/plot')

rd.files()

a = rd.readData()

# print(a[0])

a[0].plot(sharex=True, subplots=True)
plt.show()
