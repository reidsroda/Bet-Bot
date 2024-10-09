from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


#Initializing Driver
driver = webdriver.Chrome()
driver.get("https://rockcitywagers.com/")
driver.maximize_window()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Setting Static Variables
username = "ACR75470"
password = "P9N7"
wait = WebDriverWait(driver, 30)
bet_amount = 15


#Data Storage
Live_Lines = pd.DataFrame(columns = ["Team1", "Team2", "Over_Line", "Over_Odds", "Under_Line", "Under_Odds", "Time"])
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
time.sleep(11)
iframe = driver.find_element(By.ID, 'ultra-live')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, "//*[text()='Basketball']").click()
time.sleep(4)


#Setting Webpage Length Variables
event_container = driver.find_element(By.CLASS_NAME, "event--container")
total_height = driver.execute_script("return arguments[0].scrollHeight", event_container)
scroll_main = driver.find_element(By.ID, "scrollbar-main") 

#Scroll to Bottom of Webpage to Load All Data
x = 0
while True:
    driver.execute_script("arguments[0].scrollBy(0, 250)", scroll_main)
    time.sleep(1)
    x += 250
    if x > (total_height - 250):
        break

#Function to Place Bets        
#Bug during error testing: Will not recognize the type of error by text
def place_bet(Prematch_Total):
    bet_slide = driver.find_element(By.CLASS_NAME, "bet-list")
    bet_slide.find_element(By.CLASS_NAME, "form-control").click()
    bet_slide.find_element(By.CLASS_NAME, "form-control").clear()
    bet_slide.find_element(By.CLASS_NAME, "form-control").send_keys(bet_amount)
    time.sleep(3)
    #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
    
    #Check for errors: insufficient funds, min bet, odds changed, no longer available
    error_box = driver.find_element(By.CLASS_NAME, "bet-footer__container")
    """
    try: 
        error_present = error_box.find_element(By.XPATH, "//*[@id='139191531-m-5-accept']/text()")
        print(error_present)
        
        
        #Check for Not Available
        if "Not" in error_present:
            if "Accept" in error_box.find_element(By.XPATH, ".//*[contains(@class, 'fa-check-circle')]").text:
                #error_box.find_element(By.XPATH, ".//*[contains(@class, 'fa-check-circle')]").click()
                #driver.find_element(By.CLASS_NAME, "toggle-bet-slip__label_and_value").click()
                print("Error: Line No Longer Available")
        if "changed" in error_present:
            button_box = error_box.find_element(By.CLASS_NAME, "bet-odds-accept")
            accept_button = button_box.find_element(By.CLASS_NAME, "ng-binding").text
            if "Accept" in accept_button:
                accept_button.click()
                
                
            print("Error: Line has Changed")
        
    except NoSuchElementException:
        print("No Error, Could have Placed")
       
        
    driver.find_element(By.XPATH, ".//*[contains(@class, 'fa-times')]").click()
         """
               
#Scrape Live Matchup Data
def data_scraper():
    global Live_Lines
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
                    if lines[0].text != '':
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
                        Live_Lines = Live_Lines.append(new_row, ignore_index = True)
                        
                        if abs(Over_Line - Prematch_Total) > 13:
                            if Over_Line > Prematch_Total:
                                if Under_Odds > -120:
                                    #Bet Under
                                    driver.execute_script("arguments[0].scrollIntoView(true)", lines[3])
                                    lines[3].click()
                                    time.sleep(3)
                                    place_bet(Prematch_Total)
                            else:
                                if Over_Odds > -120:
                                    #Bet Over
                                    driver.execute_script("arguments[0].scrollIntoView(true)", lines[1])
                                    lines[1].click()
                                    time.sleep(3)
                                    place_bet(Prematch_Total)
                                    



#Loop Through Gamesets i times
for i in range(5):
    data_scraper()
        

#Export Live Line Data to csv file for analytics
Live_Lines.to_csv("Live_Lines_Database.csv", index = False)

                        
driver.close()