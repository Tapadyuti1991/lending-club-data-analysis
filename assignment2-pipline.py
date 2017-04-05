from configparser import ConfigParser
import csv
import logging
import luigi
import os
import requests
import shutil
from luigi.s3 import S3PathTask, S3Target, S3Client

class DownloadLendingClubDataSet(luigi.Task):

    # year = luigi.IntParameter(default=2016)
    # months = luigi.ListParameter(default=[6,7,8])
    url_list = luigi.Parameter(default='https://resources.lendingclub.com/LoanStats3a.csv.zip')

    def run(self):
        print("Successfully Downloaded and unzipped data")


    def output(self):
        return luigi.LocalTarget('./downloadedData/')

class MergeDataDownloaded(luigi.Task):
    """ Downloading each file of taxi data for each url from the repo. """
    def requires(self):
        return DownloadLendingClubDataSet()

    def input(self):
        return luigi.LocalTarget('./downloadedData/')

    def run(self):
        print("Successfully Merged data")
        #add code to merge file

    def output(self):
        file_name='Merged.csv'
        return luigi.LocalTarget('./downloadedData/{}'.format(file_name))


class HandleMissingData(luigi.Task):
    """ Downloading each file of taxi data for each url from the repo. """
    def requires(self):
        return MergeDataDownloaded()

    def input(self):
        return luigi.LocalTarget('./downloadedData/Merged.csv')

    def run(self):
        print("Successfully Done with Preporcessing ")

    def output(self):

        file_name='Processed.csv'
        return luigi.LocalTarget('./downloadedData/{}'.format(file_name))


class UploadDataToS3(luigi.Task):

    """ Download each file, and save it locally to /tmp/taxi_data """
    #s3_path = luigi.Parameter()
    local_path = luigi.Parameter()
    AWS_ACCESS_KEY = luigi.Parameter()
    AWS_SECRET_KEY = luigi.Parameter()

    # def requires(self):
    #     return DownloadTaxiUrls()

    def run(self):
       client = S3Client(self.AWS_ACCESS_KEY, self.AWS_SECRET_KEY)
       client.s3.create_bucket('pranjal')
       client.put(self.local_path, 's3://pranjal')
       t = S3Target('s3://mybucket/tempfile', client=client)

    def output(self):
        print("Uploaded successfully")
