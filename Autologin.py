
# coding: utf-8

# In[40]:



# In[9]:

# to run on your local/notebook, install chrome webdriver >> $ npm install chromedriver
# the .exe needs to be alongside python file
# for docker, the dockerfile should do it.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79

from selenium.webdriver.chrome.options import Options

# from bs4 import BeautifulSoup # to-do docker install ????
import os.path
# import re
import pandas as pd
import time


import zipfile



EMAIL = input("Username : ")
PASSWORD = input("Password : ")

LOGIN_URL = 'https://www.lendingclub.com/account/gotoLogin.action'
POST_LOGIN_URL ='https://www.lendingclub.com/info/download-data.action'

# usernameStr = input("username : ")
# passwordStr = input("password : ")


def main():
    
    browser = login_with_selenuim()
    print("Starting program")
    
    
    get_content(browser)
    
def login_with_selenuim():
    
    print("Login with selenium")
    browser = webdriver.Chrome() # to-do- docker or regular. exe needs to be in path
    cwd = os.getcwd()
    create_directory("Data/Sample_Data")
    download_path = os.path.join(cwd,"Data/Sample_Data")
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_path}
    chromeOptions.add_experimental_option("prefs",prefs)
#     chromedriver = cwd
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    
   
    browser.get(LOGIN_URL)
    try:
        
        username = browser.find_element_by_id('email')
        username.send_keys(EMAIL)

        password = browser.find_element_by_id('password')
        password.send_keys(PASSWORD)

        signInButton = browser.find_element_by_id("master_accountSubmit")
        signInButton.click()

        
#         loanStatsDropdown
        
#         ZIP_URL_PREFIX = "https://resources.lendingclub.com/secure/LoanStats3a_securev1.csv.zip?"
#         ZIP_URL_SIGNATURE="signature=Rm7e3KMR6B3r%2FzOvPoB1BI6AwV4%3D&issued=1491352214463"
        
#         browser.get((ZIP_URL_PREFIX+ZIP_URL_SIGNATURE))

#         login_success = browser.find_element_by_xpath("master_banner-wrapper")
#         print("Success : ",login_success)
        
    except Exception as e:
        print("Invalid credentials")

    time.sleep(5)

#     browser.execute_script('''window.open("https://www.lendingclub.com/info/download-data.action");''')
    browser.get((POST_LOGIN_URL))
    
    
    return browser;
    
    
def get_content(browser):
    print("Creating directory")
    
    
    create_directory("Data/DOWNLOAD_LOAN_DATA")
    
    print("current url >> " ,browser.current_url)

#     html = browser.page_source
# #         print('html >> ',html)
#     soup = BeautifulSoup(html, "html.parser")
#     print('soup >> ',soup.findAll('div',{'class':'left-col'}))
    

   
    for i in range(0,8):
#         browser.find_element_by_css_selector("a#currentLoanStatsFileName").click()
        time.sleep(5)
#         print(i)
        browser.find_element_by_css_selector("select#loanStatsDropdown > option[value='"+str(i)+"']").click()
        time.sleep(5)
        browser.find_element_by_css_selector("a#currentLoanStatsFileName").click()
        
    
    

    """
    quantity = input("Single / multiple files Select S/M :")
    try:
        if(quantity == "S"):
            year1 =input("Year (1999-2016): ")
            year2 =year1
        elif(quantity == "M"):
            year1 = input("Start year (1999-2016): ")
            year2 = input("Start year (1999-2016): ")
            if(year2 < year1):
                print("Innapropriate year range")
                get_content(browser)        
        else:
            print("Please enter appropriate years")
            get_content(browser)
            
        year1_int = int(year1)    
        year2_int = int(year2)
#         print("Downloading files ",year1_int," to ",year2_int )
    except Exception as e:
        print("Please enter appropriate input")
        get_content(browser)
            
#     search_string = "sample_"+year
    
    
#     html = browser.page_source
#     print("Searching files in "+html)
    
#     soup = BeautifulSoup(html, "html.parser")
#     print(soup)

    for file in range(year1_int,year2_int+1):
#             print("a[href*='download.php?f=sample_"+str(file)+"']")
#             browser.find_element_by_css_selector("a[href*='down'")
            sample_file_link = browser.find_element_by_css_selector("a[href*='download.php?f=sample_"+str(file)+"']")
            print("Downloading files")
            sample_file_link.click()
        
        
    for file in range(year1_int,year2_int+1):
#             print("a[href*='download.php?f=sample_"+str(file)+"']")
#             browser.find_element_by_css_selector("a[href*='down'")
                
            print("Extracting files from zip")
            zippedFolder = "Data/Sample_Data/sample_"+str(file)+".zip"
            while not os.path.exists(zippedFolder):
                time.sleep(1)

            if os.path.isfile(zippedFolder):
                # read file
                dir_name =  "Data/Sample_Data/sample_"+str(file)

                zip_ref = zipfile.ZipFile(zippedFolder).extractall(dir_name) # create zipfile object
#                 zip_ref.close()

                origination_file = "sample_orig_"+str(file)+".txt" 
                performance_file = "sample_svcg_"+str(file)+".txt"  

                origination_file_path =dir_name+"/"+origination_file
                performance_file_path =dir_name+"/"+performance_file

#                 print("Searching performance file path ",performance_file_path)

                data = pd.read_csv(performance_file_path, sep="|", header = None)
                print("Performance Dataframe for sample_"+str(file))
                print(data.head())
            else:
                raise ValueError("%s isn't a file!" % file_path)
    """
    #     browser.close()   

def create_directory(path):
    
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
                    

if __name__ == '__main__':
    main()

