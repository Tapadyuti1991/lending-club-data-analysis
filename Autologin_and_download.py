
# coding: utf-8

# In[ ]:


# to run on your local/notebook, install chrome webdriver >> $ npm install chromedriver
# the .exe needs to be alongside python file
# for docker, the dockerfile should do it.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#to use custom browser >> say bye bye to chromedriver hastles !!
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# REF : [1] https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79

from selenium.webdriver.chrome.options import Options

# from bs4 import BeautifulSoup # to-do docker install ????
import os.path
# import re
import pandas as pd
import time


import zipfile

cwd = os.getcwd()
folder = os.path.join(cwd,"Data/DOWNLOAD_LOAN_DATA")

EMAIL = input("Username : ")
PASSWORD = input("Password : ")

LOGIN_URL = 'https://www.lendingclub.com/account/gotoLogin.action'
POST_LOGIN_URL ='https://www.lendingclub.com/info/download-data.action'


def main():
    
    browser = login_with_selenuim()
    print("Starting program")
    
    
#     get_content(browser)
    
def login_with_selenuim():
    
    print("Login with selenium")
    browser = webdriver.Chrome() # to-do- docker or regular. exe needs to be in path
    
#     browser = webdriver.Remote(command_executor='http://192.168.99.101:4444/wd/hub',
#          desired_capabilities=DesiredCapabilities.CHROME)
    
    create_directory("Data/DOWNLOAD_LOAN_DATA")
    
    download_path = os.path.join(cwd,"Data/DOWNLOAD_LOAN_DATA")
    
    chromeOptions = webdriver.ChromeOptions()
    
    prefs = {"download.default_directory" : download_path}
    
    chromeOptions.add_experimental_option("prefs",prefs)
    
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    
   
    browser.get(LOGIN_URL)
    try:
        
        username = browser.find_element_by_id('email')
        username.send_keys(EMAIL)

        password = browser.find_element_by_id('password')
        password.send_keys(PASSWORD)

        signInButton = browser.find_element_by_id("master_accountSubmit")
        signInButton.click()

        
    except Exception as e:
        print("Invalid credentials")
        
#   Required for cookies to settle
    time.sleep(5)
    
##    optional to-do opens new tab for the post_login_url
#     browser.execute_script('''window.open("https://www.lendingclub.com/info/download-data.action");''')

##  opens post_login_url in the existing browser
    browser.get((POST_LOGIN_URL))
    print("Navigating to url >> " ,browser.current_url)
    
    
    return browser;
    
    
def get_content(browser):
    
    #Downloading data
    print("Started : Downloading data")  
    
    for i in range(0,8):
        time.sleep(2)
        browser.find_element_by_css_selector("select#loanStatsDropdown > option[value='"+str(i)+"']").click()
        time.sleep(5)
        browser.find_element_by_css_selector("a#currentLoanStatsFileName").click()
        
    time.sleep(1)
    print("Finished : Downloading data")  
    
    #     browser.close()   #optional to-do $$$$
    
    #Unzip/Extract files
    print("Started : Unzip/Extract files")
    
    
    for item in os.listdir(folder):
        if item.endswith(".zip"): 
            file_name = folder+"/"+item
            zipfile.ZipFile(file_name).extractall(folder)
            os.remove(file_name) #optional to-do $$$$$$
            
    print("Finished : Unzip/Extract files")
    
    merge_data()
    
     

    """
    

    #put unused code here !!!!
    
    
    """
   
    
    
def merge_data():
   
    print("Started : Prepare files for merge")
    df_list = []
    
    #check inorder to avoid inclusion in merge to be tested to-do $$$$
    mergedFile = folder+"\\CombinedData.csv"
    if os.path.exists(mergedFile):   
        os.remove(mergedFile)
      
    for filename in os.listdir(folder):
        df_list.append(pd.read_csv(filename,skiprows=1,low_memory=False))
        
    combined_csv = pd.concat(df_list)
    combined_csv.to_csv(folder+"\CombinedData.csv", index=False )
    
    print("Finished : Merging files to CombinedData.csv ")
    
    print(combined_csv.head())
    
       
def create_directory(path):
    
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
                    

if __name__ == '__main__':
    main()


# In[ ]:

# ### TEST CODE
# import os.path
# # import re
# import pandas as pd

# import glob
# #read all csvs
# cwd = os.getcwd()

# folder = os.path.join(cwd,"Data\DOWNLOAD_LOAN_DATA")

    
# interesting_files = glob.glob(folder+"\*.csv") 
# df_list = []
# for filename in sorted(interesting_files):
    
#     if(filename == 'CombinedData.csv'):    
#         os.remove(filename)
#     else:    
#         df_list.append(pd.read_csv(filename,skiprows=1,low_memory=False))
# combined_csv = pd.concat(df_list)

# print(combined_csv.head())
# # print(folder+"\Combined2.csv")
# # print(len(df_list))
# combined_csv.to_csv(folder+"\CombinedData.csv", index=False )


# In[ ]:

# mergedFile = folder+"\\Combined2.csv"
# if os.path.exists(mergedFile):   
#     os.remove(mergedFile)
# print(mergedFile)

# # Permission eroor, file being used by python

