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
driver.get("https://www.betonline.ag/")
driver.maximize_window()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Setting Static Variables
username = "Sroda28@yahoo.com"
password = "Titans28"
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
time.sleep(10)
layout = driver.find_element(By.CLASS_NAME, "layout__main")
shadow_host = layout.find_element(By.TAG_NAME, "header-navigation")
shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)

# Find an element within the shadow DOM
overlay = shadow_root.find_element(By.CLASS_NAME, "main-container")
next_overlay = overlay.find_element(By.XPATH, ".//*[contains(@class, 'slot-wrapper')]")
next_overlay.find_element(By.XPATH, ".//*[contains(@class, 'root')]").click()
time.sleep(10)


driver.find_element(By.ID, "email").send_keys(username)
time.sleep(2)
driver.find_element(By.ID, "login-password").send_keys(password)
time.sleep(2)

driver.find_element(By.ID, 'login').click()
time.sleep(10)


driver.close()