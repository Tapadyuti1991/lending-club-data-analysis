import luigi
import pymssql
class DownloadLendingClubDataSet(luigi.Task):

    def run(self):
        # end whtever needs to be run

    def output(self):
        #save file to Data directory
        return luigi.LocalTarget('/Data/')

# if __name__ == '__main__':
#     luigi.run(['HelloWorldTask', '--workers', '1', '--local-scheduler'])
