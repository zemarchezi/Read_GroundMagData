# coding=utf-8
# author: jpmarchezi
from __future__ import print_function
import os, re, ssl, urllib, sys, fnmatch
from ftplib import FTP

class DataDownloader():
    def __init__(self, hostname, user='', passwd=''):
        # Parametros
        self.host = hostname
        self.user = user
        self.passwd = passwd
        self.directory = None
        self.ftp = None
        self.output = None
        self.downfile = None
        self.ctx = None

    def set_user_and_password(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def set_output_directory(self, output):
        self.output = str(output)

    def connectFTP(self):
        try:
            self.ftp = FTP(str(self.host), user=str(self.user), passwd=str(self.passwd))
            self.ftp.login()
            print('Connected to: ' + str(self.host))
        except Exception as e:
            print(e)

    def set_directoryFTP(self, directory):
        # # self.directory = '/pub/data/rbsp/rbsp%s/l%s/ect/%s/sci/rel03/%s/' % (probe.lower(),str(level),str(date.year), instrument.lower())
        # folder = '/pub/data/rbsp/rbsp%s/l%s' % (probe.lower(),str(level))
        # directory = get_all_dirs_ftp(, instrum)
        # if instrum == 'rept' or instrum == 'mageis' or instrum == 'hope':
        #     self.directory = directory + '/sectors/rel03/%s/' % (year)
        self.directory = directory
        try:
            self.ftp.cwd(directory)
            print('..')
        except Exception as e:
            print('Failed to set directory.\n' + str(e))

    def download_one_dataFTP(self, filename):
        root_dirs = self.ftp.nlst() # Lists all the files in the directory
        try:
            regex = re.compile(filename)
            # Find the file containing the part of the given
            aa = [m.group(0) for l in root_dirs for m in [regex.search(l)] if m]
            self.ftp.retrbinary(str('RETR ' + aa[0]), open(self.output + aa[0], 'wb').write)
            print("Downloaded: " + str(aa[0]))
        except Exception as e:
            print(e)


    # HTTP ##

    #

    def set_directoryHTTP(self, directory, date):
        self.date_ini = '%04d%02d%02d' % (date.year, date.month, date.day)
        self.date_end = '%04d%02d%02d' % (date.year, date.month, date.day)
        self.directory = directory

    def connectHTTP(self):
        try:
            # Certificates of access
            self.ctx = ssl.create_default_context()
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE
            ssl._create_default_https_context = ssl._create_unverified_context
            # open the url
            self.http = urllib.urlopen(self.host + self.directory, context=self.ctx)
            self.downfile = urllib.URLopener()
            print('Connected to: ' + str(self.host + self.directory))
        except Exception as e:
            print(e)

    def download_one_dataHTTP(self, filename, flag=0):
        # read all the content of the page
        root_dirs = self.http.readlines()
        try:
            regex = re.compile(filename)
            aa = []
            # extract the desired filename
            # print (filename)
            if flag == 0:
                aa = [m.group(0) for l in root_dirs for m in [regex.search(l)] if m][0].split('"')[7]
            if flag == 1:
                aa = [m.group(0) for l in root_dirs for m in [regex.search(l)] if m][0].split('"')[5]
            # print (aa)
            # dowload the file
            self.downfile.retrieve(self.host + self.directory + aa, self.output + aa)
            print('Downloaded: ' + aa)
        except Exception as e:
            print (e)

    def download_ACEfiles(self):
        filename = 'mag_level2_data_16sec_'+self.date_ini+'_to_'+self.date_end+'.txt'
        try:
            self.downfile.retrieve(self.host + self.directory, self.output + filename)
            print('Downloaded: ' + filename)
        except Exception as e:
            print (e)
