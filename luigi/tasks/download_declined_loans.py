import luigi
import pymssql

import mechanicalsoup
import argparse
import time
#Downloading data
from zipfile import ZipFile
import urllib
from tempfile import mktemp
import os

class DownloadLendingClubDataSet(luigi.Task):

    def run(self):
        # end whtever needs to be run

        #Create dir for download
        path = "Data/DECLINED_LOAN_DATA"
        try:
        if not os.path.exists(path):
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        
        
        #constants
        POST_LOGIN_URL ='https://www.lendingclub.com/info/download-data.action'
        cwd = os.getcwd()
        destDir = os.path.join(cwd,"Data/DECLINED_LOAN_DATA")

        browser = mechanicalsoup.Browser() #Browser

        # we do not need login for rejected loan complete data
        page3 = browser.get(POST_LOGIN_URL)

        print("Successfully navigated to ",page3.soup.title.text," [",page3.url,"]")

        print("Started : Downloading declined loan data")  

        #scrape
        download_file_string = page3.soup.select("div#rejectedLoanStatsFileNamesJS")[0].text

        download_file_list = download_file_string.split("|")

        initial_path = "https://resources.lendingclub.com/"

        #download
        for sec_filename in download_file_list:
            try:
                if(len(sec_filename) >0):
                    theurl = initial_path+sec_filename
        #             print(theurl)
                    filename = mktemp('.zip')
                    name, hdrs = urllib.request.urlretrieve(theurl, filename)
                    thefile=ZipFile(filename)
                    thefile.extractall(destDir)
                    thefile.close()
            except Exception as e:
                print("URL : "+sec_filename+" not found "+e)
                

        time.sleep(1)
        print("Finished : Downloading declined loan data")

    def output(self):
        #save file to Data directory
        return luigi.LocalTarget('/Data/DECLINED_LOAN_DATA')

# if __name__ == '__main__':
#     luigi.run(['HelloWorldTask', '--workers', '1', '--local-scheduler'])
