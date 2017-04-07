import luigi
import pymssql
import os.path
import pandas as pd
class MergeDataDownloaded(luigi.Task):

    def run(self):
        # end whtever needs to be run
        cwd = os.getcwd()
        folder = os.path.join(cwd,"Data/DOWNLOAD_LOAN_DATA")
        output_folder = os.path.join(cwd,"Data/")
        print("Started : Prepare files for merge")
        df_list = []
        
        #check inorder to avoid inclusion in merge to be tested to-do $$$$
        mergedFile = output_folder+"/CombinedData.csv" #check / \\  >> \
        if os.path.exists(mergedFile):   
            os.remove(mergedFile) ## just os import required??? to-do $$$$
        
        for filename in os.listdir(folder):
            df_list.append(pd.read_csv(filename,skiprows=1,low_memory=False))
            
        combined_csv = pd.concat(df_list)
        combined_csv.to_csv(output_folder+"/CombinedData.csv", index=False ) #check / \\ \
        
        print("Finished : Merging files to CombinedData.csv ")
        
        print(combined_csv.head())

    def output(self):
        #save file to Data directory
        return luigi.LocalTarget('/Data/') ## check to-do $$$

# if __name__ == '__main__':
#     luigi.run(['HelloWorldTask', '--workers', '1', '--local-scheduler'])
