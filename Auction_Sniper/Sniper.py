#******************************************************************************************************************************************************
#
#                                                               RPA - The Action Sniper 
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
from pathlib import Path


class Auction: 
    def __init__(self, cpath):
        self.SITE_LINK = "https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-auctionsniper.html"
        self.SITE_MAP = {
            "buttons": {   
                "accept-cookies": {
                    "xpath": "/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]"

                },
                "community": {
                    "xpath": "/html/body/div[1]/div/div/div/div[3]/a[1]/button"
                }, 
                "quick_bid": {
                    "xpath": "/html/body/section[2]/div/div/main/article[1]/div/aside[2]/div/p[3]/a[1]"
                },
                "place_bid": {
                    "xpath": "/html/body/div[2]/div/div/div[3]/button[2]"
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
                "title": {
                    "xpath": "/html/body/section[1]/div/h2"
                },
                "price": {
                    "xpath": "/html/body/section[2]/div/div/main/article[1]/div/aside[2]/div/input"
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

            "Reads": {
                "watch": {
                    "xpath": "/html/body/section[2]/div/div/main/article[1]/div/aside[2]/div/span[2]"
                }, 
                "Accuracy": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[3]/div/div[2]/h3"
                            
                },
                "time": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[2]/div/div[2]/h4"
                                
                },
                "token": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[2]/div/span[2]/input"
                }                

            },
            "selectors": {
                
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
                    sleep(15)
                    # aguarda elemento da page principal
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["title"]["xpath"])))
                    break
                except:
                    self.launch()
                    if n == 3:
                        raise Exception('error a tentar logar')
                    
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


    def loop_work(self, price):
        try:
            # inicia o loop para o user em false 
            option_flag = False

            while True:
                
                # realiza a lietura do tempo no elemento 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["watch"]["xpath"])))
                clock = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["watch"]["xpath"]).text
                print(clock)
                
               
                # verifica se é 1 ou mais proximo 
                if clock == '1 seconds':
                    print('mestre entrei na function')
                    # inputa o valor do leilão 
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["price"]["xpath"])))
                    self.driver .find_element(By.XPATH, self.SITE_MAP["inputs"]["price"]["xpath"]).send_keys(price)
                    # aperta o botão para dar o lance 
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["quick_bid"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["quick_bid"]["xpath"]).click()
                    # confirma o lance 
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["place_bid"]["xpath"])))
                    self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["place_bid"]["xpath"]).click()
                    sleep(30)
                    break
                # verifica se é a mensagem final do elemnto oclock javascript
                elif clock == 'Auction Ended':
                    print('perdeu o lance !!')
                # se não for continua o loop 
                else:
                    print('mestre estou com erro')
            
            # result 
            # read result time  
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["time"]["xpath"])))
            time = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["time"]["xpath"]).text
            # read accuracy 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["Accuracy"]["xpath"])))
            accuracy = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["Accuracy"]["xpath"]).text
            
            print(f'O tempo remanescente pelo robot é de: {time} e accuracy: {accuracy}')
            # armazena o token 
            self.token = self.driver.find_element(By.XPATH, self.SITE_MAP["Reads"]["token"]["xpath"]).get_attribute("value")
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

            return option_flag
                    


        except Exception as error: 
            traceback.print_exc()
            print(error)
            
    def close(self):
        self.driver.close()
    
try: 
    for n in range(0,3): 
        Rpa = Auction(r"c://")   # digite  o local do path do seu chrome drive 
        Rpa.launch()
        Rpa.pre_login('digite seu user ','digite sua senha ' )
        certifacte = Rpa.loop_work('300')
        Rpa.close()

        if certifacte: 
            break


except Exception as error: 
        if n == 3:
            print(error)
            traceback.print_exc()
            raise Exception("error na retentativa")


















