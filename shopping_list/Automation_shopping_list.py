#******************************************************************************************************************************************************
#
#                                                               RPA - shopping list
#
#
#******************************************************************************************************************************************************

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import pandas as pd
import traceback

class Shopping_List:
    def __init__(self, cpath):
        self.SITE_LINK = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-ShoppingList.html"
        self.SITE_MAP = {
            "buttons": {
                "accept-cookies": {
                    "xpath": "/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]"
                },
                "community": {
                    "xpath": "/html/body/div[1]/div/div/div/div[3]/a[1]/button"
                },
                "download": {
                    "xpath": "/html/body/div[1]/p/a"
                },
                "add": {
                    "xpath": "/html/body/div[2]/div/form/div[1]/div[2]/button"
                },
                "submit": {
                    "xpath": "/html/body/div[2]/div/form/div[3]/button"
                }, 
                "certificate": {
                    "xpath": "/html/body/div[3]/div/div/div[4]/a"
                }, 
                "download_certificate": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[4]/div/button"
                }

            },
            "inputs": {
                "username": {
                    "xpath": "/html/body/div[3]/div[3]/div/div[2]/div/div[1]/div/div/div/div[2]/div/input",
                    "id": "42:2;a"

                },
                "password": {
                    "xpath": "/html/body/div[3]/div[3]/div/div[2]/div/div[1]/div/div/div/div[3]/div/input",
                    "id": "10:103;a"
                },
                "item": {
                    "xpath": "/html/body/div[2]/div/form/div[1]/div[1]/input"
                },
                "unique_id": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[1]/div/input"
                }, 
                "full_name": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[2]/div/input"
                },
                "company": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[3]/div/input"
                }
            
            }, 

            "Reads": {
                "accuracy": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[3]/div/div[2]/h3" 
                },
                "time": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[2]/div/div[2]/h3"
                }, 
                "token": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[2]/div/span[2]/input",
                    "id": "guidvalue"
                }

            },
            "selectors": {
                "yes": {
                    "xpath": "/html/body/div[2]/div/form/div[2]/div/div[1]/input"
                }
            }
        }

        service = Service(executable_path=cpath)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def launch(self):
        self.driver.get(self.SITE_LINK)
        sleep(5)

     
    def pre_login(self, username, password):
        try:
            for n in range(0,3):
                # aceita todos os cookies do site
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["accept-cookies"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["accept-cookies"]["xpath"]).click()
                # click community button
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["community"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["community"]["xpath"]).click()
                sleep(15)
                # input username
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, self.SITE_MAP["inputs"]["username"]["id"])))
                self.driver .find_element(By.ID, self.SITE_MAP["inputs"]["username"]["id"]).send_keys(username, Keys.ENTER)
                sleep(15)
                # input password
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["password"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["password"]["xpath"]).send_keys(password, Keys.ENTER)
                # aguarda elemento da page principal
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"])))
                break
        except Exception as error: 
            traceback.print_exc()
            print(error)
            

    def dowload_insumo(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"])))
        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"]).click()
        sleep(5)
    
    def ler_insumo(self, path):
        self.list_df = pd.read_csv(path)
        print(self.list_df)

    
    def loop_principal(self):
        option_flag = False
        try:
            # inputa item da lista 
            for index, row in self.list_df.iterrows():
                # inputa item individual por linha
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["item"]["xpath"]).send_keys(row["Favorite Food"])
                # preciona o botão para confirmar o input
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["add"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["add"]["xpath"]).click()
                sleep(2)

            # preciona o opção 'yes' em list box
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["selectors"]["yes"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["selectors"]["yes"]["xpath"]).click()
            sleep(2)
            # submit o envio da lista
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"]).click()
            sleep(10)
            
            # pega o resultado 
            time = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["time"]["xpath"]).text
            accuracy = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["accuracy"]["xpath"]).text
            self.token = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["token"]["xpath"]).get_attribute("value")

            print(time + '|' + accuracy + '|' +  str(self.token) )

            # ceritificação de conclusão 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["certificate"]["xpath"])))
            print('sucess !!')     

            while True:
                # pergunta para o usuario se ele quer certificado
                decision = input('Voce gostaria de obter o certificado ? [y/n]:')
                # decision com base nao opcao do usuario 
                if decision.lower() == "y":
                    name = input("Digite seu nome: ")
                    company = input("Digite o nome de sua empresa: ")
                    self.certificate(name, company)
                    option_flag = True
                    break
                    
                elif decision == "n": 
                    print("************Finalizando aplicacao !!*****************")
                    break

                else: 
                    print("opcao invalida, tente novamente !")
                
                
        except Exception as error: 
            print(error)

        return option_flag
    
    def controle_abas(self):
        all_tabs = self.driver.window_handles
        self.driver.switch_to.window(all_tabs[-1])

        
    def close_outras_abas(self):
        all_tabs = self.driver.window_handles
        current_tab = self.driver.current_window_handle

        for tab in all_tabs:
            if tab != current_tab:
                self.driver.switch_to.window(tab)
                self.driver.close()
        
        self.driver.switch_to.window(current_tab)


    def certificate(self, name, company):
        try:
            # clica no button para page certificado
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["certificate"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["certificate"]["xpath"]).click()
            sleep(5)
            self.controle_abas()
            
            # inputa dados no campo token , equivalente a unique id
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["unique_id"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["unique_id"]["xpath"]).send_keys(self.token)
            # inputa dados no campo campany name
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["company"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["company"]["xpath"]).send_keys(company)
            # pressiona o botão para download 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download_certificate"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["download_certificate"]["xpath"]).click()
            sleep(10)
            self.close_outras_abas()

        except Exception as error:
            traceback.print_exc()
            print(error)


    def close(self):
        self.driver.close()




for n in range(0,3):
    try:
        Rpa = Shopping_List(r"C:\Users\pc-prime\Downloads\chromedriver.exe") # digite o path do seu chromedrive 
        Rpa.launch()
        Rpa.pre_login('userxpto', 'pytho342') # digite seu login e senha do automation anywhere community 
        Rpa.dowload_insumo()
        Rpa.ler_insumo(r'C:\Users\pc-prime\Downloads\shopping-list.csv') # digite o path da pasta dowloads
        certificate = Rpa.loop_principal()
        Rpa.close()
        
        if certificate:
            break
        
    except Exception as error: 
        if n == 3:
            print(error)
            traceback.print_exc()
            raise Exception("error na retentativa")
        
    
         
    
    





































