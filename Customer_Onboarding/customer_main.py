#******************************************************************************************************************************************************
#
#                                                               RPA - Customer Onboarding 
#
#
#******************************************************************************************************************************************************


# imports 
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
import os 
import shutil
import glob
from pathlib import Path
import stat

# main class 

class Customer: 
    def __init__(self, cpath): 
        self.SITE_LINK = "https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-customeronboarding.html?_ga=2.116516358.1823181414.1712968565-1884481432.1673894428"
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
                "Register": {
                    "xpath": "/html/body/div[2]/div/form/div[8]/button"
                },
                "Ok": {
                    "xpath": "/html/body/div[3]/div/div/div[4]/button"
                },
                "certificate": {
                    "xpath": "/html/body/div[3]/div/div/div[4]/a"
                },
                "download_certificate": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[5]/div/button"
                }

            },
            "inputs": {
                "username": {
                    "xpath": "/html/body/div[3]/div[3]/div/div[2]/div/div[1]/div/div/div/div[2]/div/input",
                    "id": "42:2;a"

                },
                "password": {
                    "xpath": "/html/body/div[5]/div[3]/div/div[2]/div/div[1]/div/div/div/div[3]/div/input",
                    "id": "10:126;a"
                },
                "Customer_name": {
                    "xpath": "/html/body/div[2]/div/form/div[1]/input"
                },
                "Customer_id": {
                    "xpath": "/html/body/div[2]/div/form/div[2]/input"
                },
                "Primary_contact": {
                    "xpath": "/html/body/div[2]/div/form/div[3]/input"
                },
                "Street_address": {
                    "xpath": "/html/body/div[2]/div/form/div[4]/input"
                },
                "City": {
                    "xpath": "/html/body/div[2]/div/form/div[5]/div[1]/input"
                
                },
                "Zip": {
                    "xpath": "/html/body/div[2]/div/form/div[5]/div[3]/input"
                },
                "Email": {
                    "xpath": "/html/body/div[2]/div/form/div[6]/input"
                }, 
                "unique_id": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[1]/div/input"
                }, 
                "full_name": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[2]/div/input"
                },
                "company": {
                    "xpath": "/html/body/div/div[1]/div[2]/div/div/div[1]/form/div[4]/div/input"
                            
                }
            
            }, 
            "Combo_box": {
                "State": {
                    "xpath": "/html/body/div[2]/div/form/div[5]/div[2]/select"
                }
                
            },

            "Reads": {
                "Accuracy": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div/div[3]/div/div[2]/h3"
                },
                "time": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div/div[2]/div/div[2]/h3"
                },
                "token": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[2]/div/span[2]/input"
                }
                

            },
            "selectors": {
                "Active_discount": {
                    "yes": {
                        "xpath": "/html/body/div[2]/div/form/div[7]/div[1]/div[1]/input"
                    },
                    "no": {
                        "xpath": "/html/body/div[2]/div/form/div[7]/div[1]/div[2]/input"
                    }
                },
                "Non_disclosure": {
                    "xpath": "/html/body/div[2]/div/form/div[7]/div[2]/label/input"
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
                try:
                    try:
                        # aceita todos os cookies do site
                        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["accept-cookies"]["xpath"])))
                        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["accept-cookies"]["xpath"]).click()
                    except:
                        print('button não existe')
                    # click community button
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["community"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["community"]["xpath"]).click()
                    sleep(15)
                    # input username
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, self.SITE_MAP["inputs"]["username"]["id"])))
                    self.driver .find_element(By.ID, self.SITE_MAP["inputs"]["username"]["id"]).send_keys(username, Keys.ENTER)
                    sleep(15)
                    # input password
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, self.SITE_MAP["inputs"]["password"]["id"])))
                    self.driver.find_element(By.ID, self.SITE_MAP["inputs"]["password"]["id"]).send_keys(password, Keys.ENTER)
                    # aguarda elemento da page principal
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"])))
                    break
                except:
                    self.launch()
                    if n == 3:
                        raise Exception('error a tentar logar')
                    
        except Exception as error: 
            traceback.print_exc()
            print(error)

    def download_csv(self, path):
        # clica no botão e aguardo o ficheiro csv
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"])))
        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["download"]["xpath"]).click()
        sleep(10)
        # movendo para pasta do projeto 
        # pasta dowload padrão 
        path_download = str(Path.home() / "Downloads")
        # lista todos os arquivos com determinado nome na pasta downloads
        ficheiros = glob.glob(os.path.join(path_download, "customer-onboarding-challenge*.csv"))
        # loop para mover 
        print("os ficheiros são:", ficheiros)
        for arquivo in ficheiros:
            try: 
                # casp o arquivo não exista na pasta ainda 
                print(arquivo)
                shutil.move(arquivo, path)
                print("Arquivos movidos com sucesso!", path)
            except: 
                # lista os arquivos na pasta passada
                rarq = os.listdir(path)
                # loop para remoção do arquivos no path destino 
                for r in rarq:
                    fullname = os.path.join(path, r)
                    print("o full é:",fullname)
                    os.remove(fullname)
                    print('removido com sucesso !')
                # move os arquivos de dowloand para pasta destino
                shutil.move(arquivo, path)
                print("Arquivos movidos com sucesso!")

    
    def Read_csv(self, path):
        try:
            archive = os.listdir(path)
            for a in archive: 
                try:
                    union = os.path.join(path, a)
                    print("o aqruiv atual é:", union)
                    self.work_list = pd.read_csv(union)
                    print(self.work_list)
                except:
                    raise Exception("Não tem fecheiros disponivel para leitura")

        except Exception as error: 
            traceback.print_exc()
            print(error)

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
            sleep(15)
            self.close_outras_abas()

        except Exception as error:
            traceback.print_exc()
            print(error)

    def work_principal(self):
        try:
            # inicia flag como false para depois usuario inputar sua decisão 
            option_flag = False
            # verifica se o ficheiro possui conteudo 
            if self.work_list.empty: 
                raise Exception("O Ficheiro está vazio. Não há dados disponíveis para processar.")

            for index, row in self.work_list.iterrows():
                # preenche o customer name = Company name (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Customer_name"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Customer_name"]["xpath"]).send_keys(row["Company Name"])
                # preenche o customer ID  = customer ID (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Customer_id"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Customer_id"]["xpath"]).send_keys(row["Customer ID"])
                # preenche o primary contact  = primary contact(no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Primary_contact"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Primary_contact"]["xpath"]).send_keys(row["Primary Contact"])
                # preenche o street Address  = street Address(no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Street_address"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Street_address"]["xpath"]).send_keys(row["Street Address"])
                # preenche a City  = City (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["City"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["City"]["xpath"]).send_keys(row["City"])
                # preenche a State  = State (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Combo_box"]["State"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["Combo_box"]["State"]["xpath"]).send_keys(row["State"], Keys.ENTER)
                sleep(5)
                # preenche a zip  = zip (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Zip"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Zip"]["xpath"]).send_keys(row["Zip"])
                # preenche a Email  = Email (no ficheiro) 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Email"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Email"]["xpath"]).send_keys(row["Email Address"])
                # preenche a option YES or NO conforme ficheiro 
                # pega a linha atual no ficheiro 
                current_Offer = row["Offers Discounts"]
                current_nondis = row["Non-Disclosure On File"]
                # verifica a option a se preencher 
                if current_Offer == 'YES':
                    # preenche a option yes 
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["selectors"]["Active_discount"]["yes"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["selectors"]["Active_discount"]["yes"]["xpath"]).click()
                else: 
                    # preenche a option no  
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["selectors"]["Active_discount"]["no"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["selectors"]["Active_discount"]["no"]["xpath"]).click()
                
                if current_nondis == 'YES':
                    # verifica se deve marcar a option 
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["selectors"]["Non_disclosure"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["selectors"]["Non_disclosure"]["xpath"]).click()
                else:
                    print('option:', current_nondis)
                sleep(10)
                # clica no botão register para inputar a current linha do loop 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["Register"]["xpath"])))
                self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["Register"]["xpath"]).click()
            
            # read result 
            # read time 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["time"]["xpath"])))
            time = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["time"]["xpath"]).text
            # read accuracy 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["Accuracy"]["xpath"])))
            accuracy = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["Accuracy"]["xpath"]).text
            # armazena o token 
            self.token = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["token"]["xpath"]).get_attribute("value")
            # imprime o resultado 
            print(f'O tempo realizado pelo robot é de: {time} e accuracy: {accuracy}')

            # ceritificação de conclusão 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["certificate"]["xpath"])))   
            print('Sucess !!!')
            
            while True:
                # pergunta para o usuario se ele quer certificado
                decision = input('Voce gostaria de obter o certificado ? [y/n]:')
                # decision com base nao opcao do usuario 
                if decision.lower() == "y":
                    name = input("Digite seu nome: ")
                    company = input("Digite o nome de sua empresa: ")
                    self.certificate(name, company)
                    option_flag = True
                    print('Dowload com sucesso !!')
                    break
                    
                elif decision == "n": 
                    print("************Finalizando aplicacao !!*****************")
                    break

                else: 
                    print("opcao invalida, tente novamente !")
            
        except Exception as error: 
            traceback.print_exc()
            print(error)

        return option_flag

    def close(self):
        self.driver.close()


# looping principal 
path = r"C:\Users\pc-prime\Documents\RPA_Chalegend\Customer_Onboarding\Ficheiros" # coloque o camiho da sua pasta , onde ficara alocado os ficheiros

for n in range(0,3):
    try: 
        Rpa = Customer(r"C:\Users\pc-prime\Downloads\chromedriver.exe") # coloque o local que esta o seu chrome driver
        Rpa.launch()
        Rpa.pre_login('userxpto', 'pytho342!')  # digite seu login e senha do automation anywhere community 
        Rpa.download_csv(path)
        Rpa.Read_csv(path)
        certificate = Rpa.work_principal()
        Rpa.close()

        if certificate:
            break

    except Exception as error: 
        if n == 3:
            print(error)
            traceback.print_exc()
            raise Exception("error na retentativa")













