#******************************************************************************************************************************************************
#
#                                                               RPA - Message Decoder 
#
#
#******************************************************************************************************************************************************

from googletrans import Translator
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

# obs : para o usso da biblioteca translator do google ultilize o install -> pip install googletrans==4.0.0-rc1




class Decoder:
    def __init__(self, cpath):
         self.SITE_LINK = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-Translate.html?_ga=2.235273097.969763320.1712505848-1884481432.1673894428&_gl=1*1g9nccq*_ga*MTg4NDQ4MTQzMi4xNjczODk0NDI4*_ga_DG1BTLENXK*MTcxMjUwNTg0OS4xMy4xLjE3MTI1MTEyNzUuNjAuMC4w"
         self.SITE_MAP = {
              "buttons": {
                "accept-cookies": {
                    "xpath": "/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]"
                },
                "community": {
                    "xpath": "/html/body/div[1]/div/div/div/div[3]/a[1]/button"
                },
                "submit": {
                    "xpath": "/html/body/main/div[1]/div[1]/section/div/a"
                },
                "ok": {
                    "xpath": "/html/body/main/div[2]/div/div/div[4]/button"
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
                "response_translate": {
                    "xpath": "/html/body/main/div[1]/div[1]/section/input"
                }
                   
              },
              "reads": {
                  "title": {
                      "xpath": "/html/body/main/div[1]/div[1]/section/h1"
                  },
                  "message": {
                      "xpath": "/html/body/main/div[1]/div[1]/section/h2"
                  }, 
                  "time": {
                      "xpath": "/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/h3"
                  },
                  "accuracy": {
                      "xpath": "/html/body/main/div[2]/div/div/div[3]/div/div/div[3]/div/div[2]/h3"
                  }
              }
         }

         service = Service(executable_path=cpath)
         options = webdriver.ChromeOptions()
         options.add_experimental_option('excludeSwitches', ['enable-logging'])
         self.driver = webdriver.Chrome(service=service, options=options)
         self.driver.maximize_window()

    def Launch(self):
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
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["reads"]["title"]["xpath"])))
                break
        except Exception as error: 
            traceback.print_exc()
            print(error)
    
    def get_text(self):
        try: 
            # pegando o texto em outro idioma a ser traduzido 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["reads"]["message"]["xpath"])))
            text = self.driver .find_element(By.XPATH, self.SITE_MAP["reads"]["message"]["xpath"]).text
            print(text)
            return text

        except Exception as error:
            traceback.print_exc()
            print(error)

    def traductor(self, text):
         trans = Translator()

         translated_text = trans.translate(text, src='bg', dest='en')

         print(text)
         print(translated_text.text)

         return translated_text.text
    
    def input_response(self, response): 
        try:
            # foramtando variavel recebida 
            split = response.split(":", 1)
            final_response  = split[1]
            # inputando a resposta traduzida 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["response_translate"]["xpath"])))
            self.driver .find_element(By.XPATH, self.SITE_MAP["inputs"]["response_translate"]["xpath"]).send_keys(str(final_response))
            # concluir operação 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"])))
            self.driver .find_element(By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"]).click()
            
            # pegando resultado 
            # time
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["reads"]["time"]["xpath"])))
            time = self.driver .find_element(By.XPATH, self.SITE_MAP["reads"]["time"]["xpath"]).text
            # accuracy 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["reads"]["accuracy"]["xpath"])))
            accuracy = self.driver .find_element(By.XPATH, self.SITE_MAP["reads"]["accuracy"]["xpath"]).text
            sleep(5)
            # clicando em OK 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["ok"]["xpath"])))
            self.driver .find_element(By.XPATH, self.SITE_MAP["buttons"]["ok"]["xpath"]).click()


            print(f'O tempo de resoluçao foi: {time} e sua pontuação: {accuracy}')
            
        except Exception as error:
            traceback.print_exc()
            print(error)

    def close(self):
        self.driver.close()



# loop principal 
        
for n in range(0,3):
    try:
        Rpa = Decoder(r"C:\Users\pc-prime\Downloads\chromedriver.exe") # digite o path do seu chromedrive 
        Rpa.Launch()
        Rpa.pre_login('user', 'python321') # digite seu login e senha do automation anywhere community 
        text_t = Rpa.get_text()
        translate_t = Rpa.traductor(text_t)
        Rpa.input_response(translate_t)
        Rpa.close()
        break

    except Exception as error:
        if n == 3: 
            traceback.print_exc()
            print(error)
            raise Exception("error na retentativa")










