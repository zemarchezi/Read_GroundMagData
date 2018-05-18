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
