#******************************************************************************************************************************************************
#
#                                                               RPA - Rpa Challegend 
#
#
#******************************************************************************************************************************************************

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
import pandas as pd
import traceback

data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Challegend:
    def __init__(self): 
        self.SITE_LINK = "https://rpachallenge.com/"
        self.SITE_MAP = {
            "buttons": {
                "downloadP": {
                    "xpath": "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/a/i"
                    
                },
                "start": {
                    "xpath": "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button"
                },
                "submit": {
                    "xpath": "/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input"
                }
            },
            "inputs": {
                "first_name": {
                    "xpath":  '//input[contains(@ng-reflect-name, "labelFirstName")]' # "/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[1]/rpa1-field/div/input"
                },
                "Role_company": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelRole")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[2]/rpa1-field/div/input"
                },
                "number": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelPhone")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[3]/rpa1-field/div/input"
                },
                "Address": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelAddress")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[4]/rpa1-field/div/input"
                },
                "company_name": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelCompanyName")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[5]/rpa1-field/div/input"
                },
                "email": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelEmail")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[6]/rpa1-field/div/input"
                },
                "last_name": {
                    "xpath": '//input[contains(@ng-reflect-name, "labelLastName")]' #"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div[7]/rpa1-field/div/input"
                }
            },
            "reads": {
                "result": {
                    "xpath": "/html/body/app-root/div[2]/app-rpa1/div/div[2]/div[2]"
                }
            }
        }


        service = Service(executable_path=r"C:\Users\pc-prime\Downloads\chromedriver.exe")
        options = webdriver.ChromeOptions()
        #options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def Launch(self):
        self.driver.get(self.SITE_LINK)
        sleep(5)

    def baixar_insumo(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["downloadP"]["xpath"])))
        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["downloadP"]["xpath"]).click()
        sleep(15)


    def armazenar_inumo(self, path):
        self.df = pd.read_excel(path)
        self.df.columns = self.df.columns.str.strip()
        self.df.reset_index(drop=True, inplace=True)
        print(self.df)

    def work_step(self):
        try:
            # press start button from start challegend
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["start"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["start"]["xpath"]).click()
            sleep(2)
            
            # input fields to challegend
            for index, row in self.df.iterrows():
                # input to first name 
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["first_name"]["xpath"]).send_keys(row["First Name"])
                # input to Last Name 
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["last_name"]["xpath"]).send_keys(row["Last Name"])
                # input to Company Name 
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["company_name"]["xpath"]).send_keys(row["Company Name"])
                # input to Role in company 
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Role_company"]["xpath"]).send_keys(row["Role in Company"])
                # input to Address 
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Address"]["xpath"]).send_keys(row["Address"])
                # input to Email  
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["email"]["xpath"]).send_keys(row["Email"])
                # input to phone number  
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["number"]["xpath"]).send_keys(row["Phone Number"])
                # press button submit 
                self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"]).click()
                sleep(2)


            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["reads"]["result"]["xpath"])))
            self.result = self.driver.find_element(By.XPATH, self.SITE_MAP["reads"]["result"]["xpath"]).text
            self.result = self.result + '_' + str(data)
            print(self.result)
            
        except Exception as error:
            print(error)
            traceback.print_exc()

    def salvar_result(self, path):
        try:
            data_hora_str = data.replace(" ","-").replace(":", "-")
            name = f"result-{data_hora_str}.txt"
            path_final = path + "/" + name

            with open(path_final, "w") as archive:
                archive.write(self.result)

            print("sucess salve in:" , str(path_final))

        except Exception as error:
            print(error)
            traceback.print_exc()

    def close(self):
        self.driver.close()


try:
    Rpa = Challegend()
    Rpa.Launch()
    #Rpa.baixar_insumo()
    Rpa.armazenar_inumo(r'C:\Users\pc-prime\Downloads\challenge.xlsx')
    Rpa.work_step()
    Rpa.salvar_result(r'C:\Users\pc-prime\Downloads')
    Rpa.close()



except Exception as error:
    print(error)
    traceback.print_exc()


























