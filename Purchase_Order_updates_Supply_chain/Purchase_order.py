#******************************************************************************************************************************************************
#
#                                                               RPA - Purchase Order Updates - Supply Chain 
#
# url challenge - https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-supplychainmanagement.html?_gl=1*9f936t*_gcl_au*MjkzNjY3MzQ5LjE3MjQxMDg5OTU.*_ga*MTkwNjc3OTA0MS4xNzI0MTA4OTk2*_ga_DG1BTLENXK*MTcyNDEwODk5NS4xLjEuMTcyNDExMjQ1NC41Ny4wLjA.&_fsi=2zuaUcKr
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
import openpyxl
import os
import shutil
import glob

class Supply:
    def __init__(self, cpath) -> None:
        self.SITE_LINK = "https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-supplychainmanagement.html?_fsi=2zuaUcKr&_gl=1*3p8sjb*_gcl_au*MjkzNjY3MzQ5LjE3MjQxMDg5OTU.*_ga*MTkwNjc3OTA0MS4xNzI0MTA4OTk2*_ga_DG1BTLENXK*MTcyNDE5NTU2Mi4yLjEuMTcyNDE5NTU4MS40MS4wLjA."
        self.SITE_MAP = {
            "buttons": {
                "accept-cookies": {
                    "xpath": "/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]"
                },
                "community": {
                    "xpath": "/html/body/div[1]/div/div/div/div[3]/a[1]/button"
                },
                "download_ficheiro": {
                    "xpath": "/html/body/div[1]/div/div[2]/a" 
                },
                # # site procurement anyhere
                "sign_in": {
                    "xpath": "/html/body/div[1]/div/div/div/div/form/button[1]"
                }, 
                "submit": {
                    "xpath": "/html/body/div[2]/div/form/div[15]/div[1]/button"
                },
                # result final
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
                    "id": "43:2;a"
                },
                "password": {
                    "xpath": "/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/div[1]/div[3]/div/input",
                    "id": "10:154;a", 
                    "class": "textbox input sfdc_passwordinput sfdc input" 
                },
                "ship_date": {
                    "xpath": "/html/body/div[2]/div/form/div[2]/div[1]/input",
                    "id": "shipDate$"
                },
                "Order_tot": {
                    "xpath": "/html/body/div[2]/div/form/div[2]/div[2]/div/input",
                    "id": "orderTotal$"
                },
              # site procurement anyhere 
                "email_Adreess": {
                    "xpath": "/html/body/div[1]/div/div/div/div/form/div[1]/input"
                },
                "Procurement_Password": {
                    "xpath": "/html/body/div[1]/div/div/div/div/form/div[2]/input"
                },
                "search": {
                    "xpath": "/html/body/div[2]/div/form/div/div[2]/label/input"
                },
                # result final 
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
                "Po_number": {
                    "id": "PONumber$$NUMBER$$" 

                },
                # site procurement anyhere 
                "label": {
                    "xpath": "/html/body/div[1]/h2"
                },
                "PON": {
                    "xpath": "/html/body/div[2]/div/form/div/table/tbody/tr/td[1]",
                },
                "State": {
                    "xpath": "/html/body/div[2]/div/form/div/table/tbody/tr/td[5]"
                },
                "ship_date": {
                    "xpath": "/html/body/div[2]/div/form/div/table/tbody/tr/td[7]"
                },
                "order_total": {
                    "xpath": "/html/body/div[2]/div/form/div/table/tbody/tr/td[8]"
                },
                # result final
                "time": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[2]/div/div[2]/h3"
                },
                "Accuracy": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[1]/div[3]/div/div[2]/h3"
                }, 
                "token": {
                    "xpath": "/html/body/div[3]/div/div/div[3]/div/div[2]/div/span[2]/input"
                }

            },
            "select_box": {
                "Assigned": {
                    "xpath": "/html/body/div[2]/div/form/div[2]/div[3]/select",
                    "id": "agent$"
                }

            },
            "hyperlinks": {
                "Procurement_Anywhere": {
                    "xpath": "/html/body/div[1]/div/p/a"
                }
            }
        }

        service = Service(executable_path=cpath)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-notifications")
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
                    WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Password"]')))
                    self.driver.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(password, Keys.ENTER)
                    sleep(15)
                    # aguarda elemento da page principal
                    #WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["title"]["xpath"])))
                    break
                except:
                    self.launch()
                    if n == 3:
                        raise Exception('error a tentar logar')
                    
        except Exception as error: 
            traceback.print_exc()
            print(error)

    def Download_ficheiro(self, path):
        try:
            # click no button download para realizar a extração do ficheiro excel
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["download_ficheiro"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["download_ficheiro"]["xpath"]).click()
            sleep(30)
            
            # identifica o ultimo ficheiro excel baixado e move para pasta do projeto 
            # define pasta downloads local 
            path_download = str(Path.home() / "Downloads")
            # lista todos ficheiros com a nomenclatura na pasta downloads
            local = glob.glob(os.path.join(path_download, "StateAssignments*.xlsx"))
            # move os ficheiros para pasta do projeto
            print("Ficheiros localizados:", local)

            for ficheiro in local:
                try:
                    # se o arquivo náo existir no diretorio 
                    # lista todos os ficheiros existentes no diretorio do projeto 
                    dest = glob.glob(os.path.join(path, "StateAssignments*.xlsx"))
                    print(dest)
                    # Se o nome do ficheiro começar com StateAssignments, remove 
                    for exist_file in dest:
                        os.remove(exist_file)
                        print(f"o Ficheiro existente foi removido com sucesso: {exist_file}")

                    # tenta mover novamente caso ocorreu algum confilto 
                    shutil.move(ficheiro, path)
                    print(f"Ficheiro {ficheiro} movido com sucesso !") 

                    # guarda a varivael com nome do ficheiro 
                    leitura = os.path.join(path, os.path.basename(ficheiro))
                    print(leitura)

                except Exception as error:
                    print(f"Erro ao mover o arquivo: {error}")
                    traceback.print_exc()

                    
            # realiza a leitura do ficheiro na pasta local
            self.ficheiro_main = pd.read_excel(leitura)
            print(self.ficheiro_main)

        except Exception as error:
            traceback.print_exc()
            print(error)

    def Extract_PO_number(self): 
        try:
            self.po_numbers = []

            for n in range(1,8):
                # substitui o id do elemento pelo numero do contador 
                Id_PO = self.SITE_MAP["Reads"]["Po_number"]["id"].replace("$$NUMBER$$", str(n))
                print(Id_PO)
                # read PO Number 
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, Id_PO)))
                self.PO_read = self.driver.find_element(By.ID, Id_PO).get_attribute("value")
                print(self.PO_read)
                # formata em dicionario 
                data = {
                    "PO_Number": self.PO_read
                }
                # adciona valor lido a lista 
                self.po_numbers.append(data)

            # apresenta lista 
            print("PO Numbers encontrados:", self.po_numbers)

            # transforma em df 
            self.df_PO = pd.DataFrame(self.po_numbers)
            print(self.df_PO)

        except Exception as error: 
            traceback.print_exc()
            print(error)

    def Login_Procurement(self, email, passw):
        # click em hyperlink para abrir o Procurement Anhywhere 
         WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["hyperlinks"]["Procurement_Anywhere"]["xpath"])))
         self.driver.find_element(By.XPATH, self.SITE_MAP["hyperlinks"]["Procurement_Anywhere"]["xpath"]).click()
         self.controle_abas()
         sleep(10)

        # input username
         WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["email_Adreess"]["xpath"])))
         self.driver .find_element(By.XPATH, self.SITE_MAP["inputs"]["email_Adreess"]["xpath"]).send_keys(email)
         sleep(5)
         # input password
         WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["Procurement_Password"]["xpath"])))
         self.driver.find_element(By.XPATH, self.SITE_MAP["inputs"]["Procurement_Password"]["xpath"]).send_keys(passw)
         sleep(5)
         # click em sigin button 
         WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["sign_in"]["xpath"])))
         self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["sign_in"]["xpath"]).click()
         # aguarda label de inicio 
         WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["label"]["xpath"])))

    def controle_abas(self):
        # esperar nova aba
        # Esperar até que a nova aba seja aberta
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

        all_tabs = self.driver.window_handles
        self.driver.switch_to.window(all_tabs[-1])
  
    def close_current_aba(self):
        all_tabs = self.driver.window_handles
        current_tab = self.driver.current_window_handle

        # fecha aba atual 
        self.driver.close()
        # remove da lista de abas abertas 

        all_tabs.remove(current_tab)

        if all_tabs:
            self.driver.switch_to.window(all_tabs[0])  # Troca para a primeira aba da lista de abas abertas
        else:
            print("Nenhuma outra aba está aberta.")

    def Found_PO_Number(self, path):
        try:
            extract_list = []
            # procurar com pase no Po number 
            for index, row in self.df_PO.iterrows():
                # input username
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["inputs"]["search"]["xpath"])))
                self.driver .find_element(By.XPATH, self.SITE_MAP["inputs"]["search"]["xpath"]).clear()
                self.driver .find_element(By.XPATH, self.SITE_MAP["inputs"]["search"]["xpath"]).send_keys(row["PO_Number"],Keys.ENTER)
                # extract po. number 
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["PON"]["xpath"])))
                PON = self.driver .find_element(By.XPATH, self.SITE_MAP["Reads"]["PON"]["xpath"]).text
                # extract ship date
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["ship_date"]["xpath"])))
                date = self.driver .find_element(By.XPATH, self.SITE_MAP["Reads"]["ship_date"]["xpath"]).text
                #  extract state 
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["State"]["xpath"])))
                State = self.driver .find_element(By.XPATH, self.SITE_MAP["Reads"]["State"]["xpath"]).text
                # extract Order total 
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["Reads"]["order_total"]["xpath"])))
                totOrder = self.driver .find_element(By.XPATH, self.SITE_MAP["Reads"]["order_total"]["xpath"]).text

                # adicionando em um dicionario 
                po_data = {
                    "PO Number": PON,
                    "Ship Date": date,
                    "State": State, 
                    "Order Total": totOrder
                }

                # adiciona a lista 
                extract_list.append(po_data)

                #  transforma em df
                self.df_Extract = pd.DataFrame(extract_list)

                # transforma em excel
                self.df_Extract.to_excel(path + r'\PO_Number_Details.xlsx', index=False)

                print(self.df_Extract)   
            # fecha a aba após a extração
            self.close_current_aba()
        except Exception as error: 
                traceback.print_exc()
                print(error)
        
    def Merged_Ficheiros(self, path):
        try:
            merged_df = pd.merge(self.df_Extract, self.ficheiro_main, on='State', how='left', sort=False)
            self.filter_df = merged_df[merged_df['State'].notnull()]
            self.filter_df = self.filter_df.rename(columns={'Full Name': 'Agente'})

            # remove vazios
            self.filter_df = self.filter_df.dropna(subset=['PO Number'])

            print(self.filter_df)
            # transforma em excel
            self.filter_df.to_excel(path + r'\Extract_final.xlsx', index=False)

        except Exception as error: 
                traceback.print_exc()
                print(error)

    def Loop_Main(self):
        try:
            n = 1
            for index, row in self.filter_df.iterrows():
                
                # substitui o id do elemento pelo numero do contador 
                Id_date = self.SITE_MAP["inputs"]["ship_date"]["id"].replace("$", str(n))
                print(Id_date)
                Id_order = self.SITE_MAP["inputs"]["Order_tot"]["id"].replace("$", str(n))
                print(Id_order)
                Id_agent = self.SITE_MAP["select_box"]["Assigned"]["id"].replace("$", str(n))
                print(Id_agent)

                # inputa o campo Ship date 
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, Id_date)))
                self.driver .find_element(By.ID, Id_date).send_keys(row["Ship Date"])
                sleep(2)
                # inputa o campo Order total 
                format = row["Order Total"].replace("$", "")
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, Id_order)))
                self.driver .find_element(By.ID, Id_order).send_keys(format)
                sleep(2)
                # inputa o campo assigned 
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, Id_agent)))
                self.driver .find_element(By.ID, Id_agent).send_keys(row["Agente"])

                n += 1
            # click button submit 
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"])))
            self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["submit"]["xpath"]).click()
            sleep(10)
            

        except Exception as error: 
                traceback.print_exc()
                print(error)

    def Get_certificate(self):
        try: 
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
            self.close_current_aba()

        except Exception as error:
            traceback.print_exc()
            print(error)
    
    def Close(self):
        try:
            # fecha a aplicação
            self.driver.close()

        except Exception as error:
            traceback.print_exc()
            print(error)


try: 
    # var globais 
    path_ficheiros = r"C:\\Ficheiros" # digite sua pasta onde ficarão os logs e ficheiros do projeto 

    for n in range(0,3):
        Rpa = Supply(r"C:\chromedriver.exe") # Digite seu chrome drive
        Rpa.launch()
        Rpa.pre_login('xpto', 'aaa!') # digite seu login e senha do automation Anywhere community 
        Rpa.Download_ficheiro(path_ficheiros)
        Rpa.Extract_PO_number()
        Rpa.Login_Procurement('admin@procurementanywhere.com', 'paypacksh!p') # user e senha padão do challegend
        Rpa.Found_PO_Number(path_ficheiros)
        Rpa.Merged_Ficheiros(path_ficheiros)
        Rpa.Loop_Main()
        certificate = Rpa.Get_certificate()
        Rpa.Close()
        sleep(10)

        if certificate:
            break

except Exception as error: 
        if n == 3:
            print(error)
            traceback.print_exc()
            raise Exception("error na retentativa")    

















