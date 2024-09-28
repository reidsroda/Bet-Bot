from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
import pandas as pd
import time


driver = webdriver.Chrome()
driver.get("https://rockcitywagers.com/")
driver.maximize_window()

username = "ACR75470"
password = "P9N7"
wait = WebDriverWait(driver, 30)


#Login to Website
driver.find_element(By.NAME, "customerID").send_keys(username)
driver.find_element(By.NAME, "Password").send_keys(password)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()
time.sleep(5)


#Enter Live Betting Interface
driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div[2]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[1]/div/header/div[2]/div[1]/div[2]/div/div[1]').click()
time.sleep(7)
iframe = driver.find_element(By.ID, 'ultra-live')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, "//*[text()='Basketball']").click()
time.sleep(3)


#Scrape Matchup Data
df = pd.DataFrame(columns = ["Team1", "Team2"])

teams = driver.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team')
i = 0

for team in teams:
    if i % 2 == 0:
        test.loc[i, "Team1"] = team.text
    if i % 2 == 1:
        test.loc[i, "Team2"] = team.text
        
    
#for matchup in matchups:
#print("Team Name: " + driver.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team').text)
    
    
#new_row = {"Team1": team1, "Team2": team2}
#df = df.append(new_row, ignore_index = True)
#print(df)
time.sleep(10)



driver.close()

