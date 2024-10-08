from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
import pandas as pd
import time
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


driver = webdriver.Chrome()
driver.get("https://rockcitywagers.com/")
driver.maximize_window()

username = "ACR75470"
password = "P9N7"
wait = WebDriverWait(driver, 30)
bet_amount = 15.61

#Data Storage
df = pd.DataFrame(columns = ["Team1", "Team2", "Over_Line", "Over_Odds", "Under_Line", "Under_Odds", "Time"])
Prematch_Totals = pd.read_csv("Prematch_Totals.csv")

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
time.sleep(15)
iframe = driver.find_element(By.ID, 'ultra-live')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, "//*[text()='Basketball']").click()
time.sleep(15)

#Scrape Live Matchup Data
for i in range(10):
    matchups = driver.find_elements(By.CLASS_NAME, 'event-list__item')
    for matchup in matchups:
        class_att = matchup.get_attribute("class")
        classes = class_att.split()
        if all("block" not in cls.lower() for cls in classes):
            teams = matchup.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team')
            col_lines = matchup.find_elements(By.XPATH, ".//*[contains(@class, 'market-5')]")
            for live_line in col_lines:
                lines = live_line.find_elements(By.XPATH, ".//*[contains(@class, 'pull')]")
                if len(lines) == 4:
                    if lines[0].text:
                        team1 = teams[0].text.split(" ")[-1]
                        team2 = teams[1].text.split(" ")[-1]
                        Over_Line = float(lines[0].text[1:])
                        Over_Odds = float(lines[1].text)
                        Under_Line = float(lines[2].text[1:])
                        Under_Odds = float(lines[3].text)
                        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                        #Prematch_Total = Prematch_Totals.loc[Prematch_Totals["Team1"] == teams[0].text.split(" ")[-1], "Original_Total"][0]
                        Prematch_Total = 0
                        #new_row = {"Team1": team1, "Team2": team2, "Over_Line": Over_Line, "Over_Odds": Over_Odds, "Under_Line": Under_Line, "Under_Odds": Under_Odds, "Time": Time, "Prematch_Total": Prematch_Total}
                        new_row = {"Team1": team1, "Team2": team2, "Over_Line": Over_Line, "Over_Odds": Over_Odds, "Under_Line": Under_Line, "Under_Odds": Under_Odds, "Time": Time}
                        df = df.append(new_row, ignore_index = True)
                        if abs(Over_Line - Prematch_Total) > 13:
                            if Over_Line > Prematch_Total:
                                #Bet Under
                                lines[3].click()
                                time.sleep(5)
                                bet_slide = driver.find_element(By.CLASS_NAME, "bet-list")
                                bet_slide.find_element(By.CLASS_NAME, "form-control").send_keys(bet_amount)
                                time.sleep(2)
                                driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
                            else:
                                #Bet Over
                                lines[1].click()
                                time.sleep(5)

                        


df.to_csv("Live_Lines_Database.csv", index = False)


#Compare Live Matchup Data with Original Data
#merged_df = pd.merge(df, Prematch_Totals, on=['Team1', 'Team2'])
#merged_df.to_csv("merged_df.csv", index = False)


"""
#Determine Which Games are outside Algorithm Range
for i in range(len(merged_df)):
    if abs(merged_df.loc[i,'Over_Line'] - merged_df.loc[i,'Prematch_Total']) > 13:
        if (merged_df.loc[i,'Over_Line'] > merged_df.loc[i,'Prematch_Total']):
            print('Bet on Under: ' + merged_df.loc[i, "Team1"] + " and " + mmerged_df.loc[i, "Team2"])
        else:
            print("Bet on Over"

print(Prematch_Totals)
"""       
      
     
      

          

driver.close()