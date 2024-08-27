#******************************************************************************************************************************************************
#
#                                 RPA - Cooking click 
#
#
#******************************************************************************************************************************************************

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time 



class Cookie:
    def __init__(self):
        self.SITE_LINK = "https://orteil.dashnet.org/cookieclicker/"
        self.SITE_MAP = {
            "buttons": {
                "bolacha": {
                    "xpath": "/html/body/div[1]/div[2]/div[15]/div[8]/button"
                    
                },
                "up": {
                   "xpath": "/html/body/div[1]/div[2]/div[19]/div[3]/div[6]/div[$$NUMBER$$]"
                            
                },
                "consent": {
                    "xpath": "/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p"
                }
            }
        }
        
        service = Service(executable_path=r"C:\Users\pc-prime\Downloads\chromedriver.exe")
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()

    def abrir_site(self):
        time.sleep(2)
        self.driver.get(self.SITE_LINK)
        time.sleep(15)


    def clicar_no_cookie(self):
       self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["bolacha"]["xpath"]).click()
        

       
    def paga_melhor_up(self):
        found = False
        element = 2

        while not found:
            obj = self.SITE_MAP["buttons"]["up"]["xpath"].replace("$$NUMBER$$", str(element))
            class_obj = self.driver.find_element(By.XPATH, obj).get_attribute("class")

            if not "enabled" in class_obj:
                found = True
            else:
                element += 1
        return element - 1


    def comprar_up(self):
        obj = self.SITE_MAP["buttons"]["up"]["xpath"].replace("$$NUMBER$$", str(self.paga_melhor_up()))
        self.driver.find_element(By.XPATH, obj).click() 




try:
    Rpa = Cookie()
    Rpa.abrir_site()
    
    i = 0 

    while True:
        if i % 500 == 0 and i != 0:
            time.sleep(1)
            Rpa.comprar_up()
            time.sleep(1)
        Rpa.clicar_no_cookie()
        i += 1

except Exception as error:
    print(error)
