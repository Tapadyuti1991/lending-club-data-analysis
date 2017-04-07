import luigi

import handlingMissingValues
from luigi import configuration, s3
from luigi.s3 import S3Target, S3Client

from boto.s3.key import Key
from boto.s3.connection import S3Connection
class UploadDataToS3(luigi.Task):
    config = luigi.configuration.get_config()
    #aws_access_key_id = luigi.Parameter(config_path=dict(section='s3', name='aws_access_key_id'))
    # to-do $$$$
    #aws_secret_access_key = luigi.Parameter(config_path=dict(section='s3', name='aws_secret_access_key'))

    # def requires(self):
    #     return handlingMissingValues.HandleMissingData()

    # def input(self):
    #     return luigi.LocalTarget('/Data/Processed_Accepted.csv')


    def run(self):
        aws_access_key_id ='#self.aws_secret_access_key'
        aws_secret_access_key='#self.aws_secret_access_key'
        conn=S3Connection(aws_access_key_id,aws_secret_access_key)
        # bucket_name="lendingclubdata-team1"
        bucket = conn.create_bucket("team1_lending_club")
        # bucket=conn.get_bucket(bucket_name)

        k=Key(bucket)
        k.key = 'foobar' # to-do $$$$
        k.set_contents_from_string('This is a test of S3') # to-do $$$$
        print('upload test')


if __name__ == "__main__":

    luigi.run()
