from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException
import datetime
from datetime import datetime
import pandas as pd
import time
import warnings
import sqlite3


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


#Data Storage
Live_Lines = pd.DataFrame(columns = ["Team1", "Team2", "Over_Line", "Over_Odds", "Under_Line", "Under_Odds", "Time"])
Prematch_Totals = pd.read_csv("Prematch_Totals.csv")
conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS live_lines (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    team1 TEXT,
                    team2 TEXT,
                    initial_total DECIMAL,
                    live_total DECIMAL,
                    live_over_odds INT,
                    live_under_odds INT,
                    quarter TEXT,
                    time_remaining TIME,
                    live_time DATE,
                    date DATE) ''')

#Create another sqlite table for placed bets
cursor.execute(''' CREATE TABLE IF NOT EXISTS placed_wagers (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    team1 TEXT,
                    team2 TEXT,
                    original_total DECIMAL,
                    over_under TEXT,
                    live_total DECIMAL,
                    live_odds INT,
                    wager DECIMAL,
                    to_win DECIMAL,
                    date DATE,
                    time TIME) ''')

conn.commit()


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
time.sleep(10)
iframe = driver.find_element(By.ID, 'ultra-live')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, "//*[text()='Basketball']").click()
time.sleep(4)


#Setting Webpage Length Variables
event_container = driver.find_element(By.CLASS_NAME, "event--container")
total_height = driver.execute_script("return arguments[0].scrollHeight", event_container)
scroll_main = driver.find_element(By.ID, "scrollbar-main") 


        

#Function to Place Bets        
def place_bet(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet):
    #Input set bet amounts
    bet = bet
    bet_amount = 15
    bet_selection.click()
    time.sleep(1)
    bet_slide = driver.find_element(By.CLASS_NAME, "bet-list")
    bet_slide.find_element(By.CLASS_NAME, "form-control").click()
    time.sleep(1)
    bet_slide.find_element(By.CLASS_NAME, "form-control").clear()
    bet_slide.find_element(By.CLASS_NAME, "form-control").send_keys(bet_amount)
    time.sleep(7)
    error_words = ["Not", "Odds", "Line"]
    footer_box = driver.find_element(By.CLASS_NAME, "bet-footer__container")
    footer_messege = footer_box.find_element(By.CLASS_NAME, "ng-binding").text
    Date = datetime.now().strftime('%Y-%m-%d')
    
    #Check if error messege
    if "Not" in footer_messege or "Line" in footer_messege or "Odds" in footer_messege:
        return error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)
    
    
    
    #TO WIN
    to_win = abs((betting_odds * bet_amount / 100) if betting_odds > 0 else (100 / betting_odds * bet_amount))
    
    #Try to place bet right away
    #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
    time.sleep(5)
    try:
        #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
        
        #ADD BET TO PLACED WAGERS DATABASE 
        bet_data = (team1,team2, bet, betting_line, betting_odds, bet_amount, to_win, Date, time.time())
        cursor.execute("INSERT INTO placed_wagers (team1, team2, over_under, live_total, live_odds, wager, to_win, date, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", bet_data)
        conn.commit()
        
        driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
        time.sleep(3)
        return f"Bet Placed Right Away at {betting_line} with {betting_odds} odds"

    except NoSuchElementException:
        return error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)
        
    



def error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet):
    bet = bet
    footer_box = driver.find_element(By.CLASS_NAME, "bet-footer__container")
    footer_messege = footer_box.find_element(By.CLASS_NAME, "ng-binding").text
    bet_amount = 15
    Date = datetime.now().strftime('%Y-%m-%d')
    to_win = abs((betting_odds * bet_amount / 100) if betting_odds > 0 else (100 / betting_odds * bet_amount))
   
    
    if "Not" in footer_messege or "suspended" in footer_messege:
        try:
            #this is the accept button
            footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
            time.sleep(3)
            return
        except NoSuchElementException:
            error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)
            
    if "Line" in footer_messege:
        new_line = float(footer_messege.split(" ")[-1])
        new_odds = float(driver.find_element(By.XPATH, "//*[contains(@class, 'bet-odd-value')]").text)
        if abs(new_line - Prematch_Total) >= 13 & new_odds > -120:
            try:
                footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
                #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
                time.sleep(5)
                try:
                    #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
                    
                    #ADD BET TO PLACED WAGERS DATABASE 
                    bet_data = (team1,team2, bet, new_line, new_odds, bet_amount, to_win, Date, time.time())
                    cursor.execute("INSERT INTO placed_wagers (team1, team2, over_under, live_total, live_odds, wager, to_win, date, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", bet_data)
                    conn.commit()
        
                    driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
                    time.sleep(3)
                    return f"Bet Placed After Line Adjustment at {new_line}"
            
                except NoSuchElementException:
                    error_handler(Prematch_Total, bet_selection, new_line, new_odds, team1, team2, Date, bet)
                
            except NoSuchElementException:
                error_handler(Prematch_Total, bet_selection, new_line, new_odds, team1, team2, Date, bet)
        
    if "Odds" in footer_messege:
        new_odds = float(footer_messege.split(" ")[-1])
        if new_odds > -120:
            try:
                footer_box.find_element(By.CLASS_NAME, "bet-odds-accept").find_element(By.CLASS_NAME, "ng-binding").click()
                #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
                time.sleep(5)
                try:
                    #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
                    
                    #ADD BET TO PLACED WAGERS DATABASE 
                    to_win = abs((new_odds * bet_amount / 100) if new_odds > 0 else (100 / new_odds * bet_amount))
                    bet_data = (team1,team2, bet, betting_line, new_odds, bet_amount, to_win, Date, time.time())
                    cursor.execute("INSERT INTO placed_wagers (team1, team2, over_under, live_total, live_odds, wager, to_win, date, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", bet_data)
                    conn.commit()
        
                    driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()
                    time.sleep(3)
                    return f"Bet Placed after Odds Adjustment at {new_odds} odds"
            
                except NoSuchElementException:
                    error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)
                    
            except NoSuchElementException:
                error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)
                
    
    #driver.find_element(By.XPATH, "//*[@id='bet-slip-process-all']").click()
    time.sleep(5)
    try:
        #elem = driver.find_element(By.CLASS_NAME, "bet-footer__container").find_element(By.XPATH, ".//*[contains(@class, 'success')]")
        #ADD BET TO PLACED WAGERS DATABASE 
        bet_data = (team1,team2, bet, betting_line, betting_odds, bet_amount, to_win, Date, time.time())
        cursor.execute("INSERT INTO placed_wagers (team1, team2, over_under, live_total, live_odds, wager, to_win, date, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", bet_data)
        conn.commit()
        driver.find_element(By.XPATH, "//*[contains(@class, 'fa-times')]").click()


        time.sleep(3)
        return f"Bet Placed at {betting_line} with {betting_odds} odds"

    except NoSuchElementException:
        error_handler(Prematch_Total, bet_selection, betting_line, betting_odds, team1, team2, Date, bet)

        
                       
#Scrape Live Matchup Data
def data_scraper():
    x = 0
    while True:
        driver.execute_script("arguments[0].scrollBy(0, 250)", scroll_main)
        time.sleep(1)
        x += 250
        if x > (total_height - 250):
            break
    leagues = driver.find_elements(By.CLASS_NAME, 'panel')
    for league in leagues:
        league_name = league.find_element(By.CLASS_NAME, 'panel-title').text
        if league_name == "NBA":
            NBA = league
            break 
    try:
        matchups = NBA.find_elements(By.CLASS_NAME, 'event-list__item')
    except UnboundLocalError:
        return
    #matchups = driver.find_elements(By.CLASS_NAME, 'event-list__item')
    
    for matchup in matchups:
        class_att = matchup.get_attribute("class")
        classes = class_att.split()
        if all("block" not in cls.lower() for cls in classes):
            teams = matchup.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team')
            col_line = matchup.find_element(By.XPATH, ".//*[contains(@class, 'market-5')]")
            lines = col_line.find_elements(By.XPATH, ".//*[contains(@class, 'pull')]")
            
            if len(lines) == 4:
                if lines[0].text != '':
                    try: 
                        game_box = matchup.find_element(By.CLASS_NAME, "event-list__item__details__date")
                        quarter = game_box.find_element(By.TAG_NAME, "p").text 
                        time_unformatted = game_box.find_element(By.TAG_NAME, "time").text
                        team_1 = teams[0].text.split(" ")[-1].strip()
                        team2 = teams[1].text.split(" ")[-1]
                        Over_Line = float(lines[0].text[1:])
                        Over_Odds = float(lines[1].text)
                        Under_Line = float(lines[2].text[1:])
                        Under_Odds = float(lines[3].text)
                        Date = datetime.now().strftime('%Y-%m-%d')
                        time_obj = datetime.strptime(time_unformatted, "%M:%S")
                        game_time = time_obj.strftime("%M:%S")
                        live_time = datetime.today()
                        Prematch_Total = cursor.execute('SELECT original_total FROM prematch_totals WHERE team1=? AND date=?', (team_1,Date,)).fetchall()[0][0]
                        game_data = (team_1,team2, Prematch_Total, Over_Line, Over_Odds, Under_Odds, quarter, game_time, live_time, Date)
                        cursor.execute("INSERT INTO live_lines (team1, team2, initial_total, live_total, live_over_odds, live_under_odds, quarter, time_remaining, live_time, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", game_data)
                        
                    except ValueError:
                        continue
                    
                    conn.commit()
                    #CHECK TO SEE IF TEAM HAS ALREADY BEEN BET ON
                    
                    if "3rd" in quarter.lower() or "4th" in quarter.lower() or "overtime" in quarter.lower():
                        continue
                        
                    try:
                        data = cursor.execute('SELECT wager FROM placed_wagers WHERE team1=? AND date=?', (team_1, Date,)).fetchall()[0][0]
                        
                    except IndexError:
                        if abs(Over_Line - Prematch_Total) >= 15:
                            if Over_Line > Prematch_Total:
                                if Under_Odds > -120:
                                    #Bet Under
                                    driver.execute_script("arguments[0].scrollIntoView(true)", matchup)
                                    driver.execute_script("arguments[0].scrollBy(0, -100)", scroll_main)
                                    time.sleep(3)
                                    bet = "U"
                                    print(f"Team1: {team_1} vs. Team2: {team2} {place_bet(Prematch_Total, lines[3], Under_Line, Under_Odds, team_1, team2, Date, bet)}")
                            else:
                                if Over_Odds > -120:
                                    #Bet Over
                                    driver.execute_script("arguments[0].scrollIntoView(true)", matchup)
                                    driver.execute_script("arguments[0].scrollBy(0, -100)", scroll_main)
                                    time.sleep(3)
                                    bet = "O"
                                    print(f"Team1: {team_1} vs. Team2: {team2} {place_bet(Prematch_Total, lines[1], Over_Line, Over_Odds, team_1, team2, Date, bet)}")
    driver.execute_script("arguments[0].scrollTo(0, 0)", scroll_main)
                        
                    
                                



for i in range(1000):
    data_scraper()
    time.sleep(10)

        

cursor.close()
conn.close()
driver.close()