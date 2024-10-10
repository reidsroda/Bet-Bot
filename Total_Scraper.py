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
def place_bet(Prematch_Total, bet_selection, betting_line, betting_odds):
    #Input set bet amounts
    bet_selection.click()
    time.sleep(1)
    bet_slide = driver.find_element(By.CLASS_NAME, "bet-list")
    bet_slide.find_element(By.CLASS_NAME, "form-control").click()
    bet_slide.find_element(By.CLASS_NAME, "form-control").clear()
    bet_slide.find_element(By.CLASS_NAME, "form-control").send_keys(bet_amount)
    error_words = ["Not", "Odds", "Line"]
    footer_box = driver.find_element(By.CLASS_NAME, "bet-footer__container")
    footer_messege = footer_box.find_element(By.CLASS_NAME, "ng-binding").text
    #Check if error messege
    if "Not" in footer_messege or "Line" in footer_messege or "Odds" in footer_messege:
        return error_handler(Prematch_Total)
    
    #Set selected bet odds
    #updated_line = float(driver.find_element(By.CLASS_NAME, "bet-list").find_element(By.XPATH, ".//*[contains(@class, 'bet-odd-name__button-shown')]").text.split(" ")[-1])
    
    updated_odds = float(driver.find_element(By.CLASS_NAME, "bet-list").find_element(By.XPATH, ".//*[contains(@class, 'bet-odd-value')]").text)
    
    
    
    #Try to place bet right away
    #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
    try:
        #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
        driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
        time.sleep(3)
        return f"Bet Placed Right Away at {betting_line} with {updated_odds} odds"

    except NoSuchElementException:
        return error_handler(Prematch_Total)
        
    



def error_handler(Prematch_Total):
    footer_box = driver.find_element(By.CLASS_NAME, "bet-footer__container")
    footer_messege = footer_box.find_element(By.CLASS_NAME, "ng-binding").text
    if "Not" in footer_messege:
        try:
            #this is the accept button
            footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
            time.sleep(3)
            return
        except NoSuchElementException:
            error_handler(Prematch_Total)
            
    if "Line" in footer_messege:
        new_line = float(footer_messege.split(" ")[-1])
        if abs(new_line - Prematch_Total) >= 13:
            try:
                footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
                #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
                time.sleep(5)
                try:
                    #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
                    driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
                    time.sleep(3)
                    return f"Bet Placed After Line Adjustment at {new_line}"
            
                except NoSuchElementException:
                    error_handler(Prematch_Total)
                
            except NoSuchElementException:
                error_handler(Prematch_Total)
        
    if "Odds" in footer_messege:
        new_odds = float(footer_messege.split(" ")[-1])
        if new_odds > -120:
            try:
                footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
                #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
                time.sleep(5)
                try:
                    #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
                    driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
                    time.sleep(3)
                    return f"Bet Placed after Odds Adjustment at {new_odds} odds"
            
                except NoSuchElementException:
                    error_handler(Prematch_Total)
                    
            except NoSuchElementException:
                error_handler(Prematch_Total)
                
    #This part is a little sketchy, updated line/odds change to a drop down if they have changed   
    updated_line = float(driver.find_element(By.CLASS_NAME, "bet-list").find_element(By.XPATH, ".//*[contains(@class, 'bet-odd-name__button-shown')]").text.split(" ")[-1])
    
    updated_odds = float(driver.find_element(By.CLASS_NAME, "bet-list").find_element(By.XPATH, ".//*[contains(@class, 'bet-odd-value')]").text)
    
    if abs(updated_line - Prematch_Total) >= 13:
        if updated_odds > -120:
            #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
            time.sleep(5)
            try:
                #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
                driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
                time.sleep(3)
                return f"Bet Placed at {updated_line} with {updated_odds} odds"

            except NoSuchElementException:
                error_handler(Prematch_Total)

        
                       
#Scrape Live Matchup Data
def data_scraper():
    global Live_Lines
    leagues = driver.find_elements(By.CLASS_NAME, 'panel')
    for league in leagues:
        league_name = league.find_element(By.CLASS_NAME, 'panel-title').text
        if league_name == "NBA":
            NBA = league
    
    matchups = NBA.find_elements(By.CLASS_NAME, 'event-list__item')
    for matchup in matchups:
        class_att = matchup.get_attribute("class")
        classes = class_att.split()
        if all("block" not in cls.lower() for cls in classes):
            teams = matchup.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team')
            col_line = matchup.find_element(By.XPATH, ".//*[contains(@class, 'market-5')]")
            lines = col_line.find_elements(By.XPATH, ".//*[contains(@class, 'pull')]")
            if len(lines) == 4:
                if lines[0].text != '':
                    team1 = teams[0].text.split(" ")[-1]
                    team2 = teams[1].text.split(" ")[-1]
                    Over_Line = float(lines[0].text[1:])
                    Over_Odds = float(lines[1].text)
                    Under_Line = float(lines[2].text[1:])
                    Under_Odds = float(lines[3].text)
                    Time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                    
                    #FIX THIS SHIT TO MATCH WITH PREMATCH TOTAL
                    #Prematch_Total = Prematch_Totals.loc[Prematch_Totals["Team1"] == team1, "Original_Total"]
                    Prematch_Total = 0
                    #new_row = {"Team1": team1, "Team2": team2, "Over_Line": Over_Line, "Over_Odds": Over_Odds, "Under_Line": Under_Line, "Under_Odds": Under_Odds, "Time": Time, "Prematch_Total": Prematch_Total}
                    new_row = {"Team1": team1, "Team2": team2, "Over_Line": Over_Line, "Over_Odds": Over_Odds, "Under_Line": Under_Line, "Under_Odds": Under_Odds, "Time": Time}
                    Live_Lines = Live_Lines.append(new_row, ignore_index = True)
                    #CHANGE THIS TO FIT MODEL
                    if abs(Over_Line - Prematch_Total) >= 0:
                        if Over_Line > Prematch_Total:
                            if Under_Odds > -150:
                                #Bet Under
                                driver.execute_script("arguments[0].scrollIntoView(true)", matchup)
                                time.sleep(3)
                                print(f"Team1: {team1} vs. Team2: {team2} {place_bet(Prematch_Total, lines[3], Under_Line, Under_Odds)}")
                        else:
                            if Over_Odds > -150:
                                #Bet Over
                                driver.execute_script("arguments[0].scrollIntoView(true)", matchup)
                                time.sleep(3)
                                print(f"Team1: {team1} vs. Team2: {team2} {place_bet(Prematch_Total, lines[1], Over_Line, Over_Odds)}")
                                


"""
#Loop Through Gamesets i times
for i in range(5):
    data_scraper()
"""


#Loop that will stay active until a bet is place, when ready input this to loop inside the place_bet function
"""
while True:
    try:
        elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
        print("Bet Placed!")
        #Exit active bet slip
        driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "bet-slip-badge").click()
        time.sleep(2)
        break
    except NoSuchElementException:
        continue
"""
        
data_scraper()
#Export Live Line Data to csv file for analytics
Live_Lines.to_csv("Live_Lines_Database.csv", index = False)

                        
driver.close()