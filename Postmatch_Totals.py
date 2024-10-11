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

#Initiate Web Driver
#driver = webdriver.Chrome()
#driver.get("https://www.cbssports.com/nba/scoreboard/20241010/")
#driver.maximize_window()
#time.sleep(1)

#Data Storage
conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS postmatch_totals (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    team1 TEXT,
                    team1_Q1 INTEGER,
                    team1_Q2 INTEGER,
                    team1_Q3 INTEGER,
                    team1_Q4 INTEGER,
                    team2 TEXT,
                    team2_Q1 INTEGER,
                    team2_Q2 INTEGER,
                    team2_Q3 INTEGER,
                    team2_Q4 INTEGER,
                    Total INTEGER,
                    date DATE) ''')
                   

conn.commit()
cursor.close()
conn.close()

#driver.quit()

"""

games = driver.find_elements(By.XPATH, "//*[contains(@class, 'single-score-card')]")

for game in games:
    teams = driver.find_elements(By.CLASS_NAME, "team-name-link")
    team1 = teams[0].text
    team2 = teams[1].text
    totals = game.find_elements(By.CLASS_NAME, "total").text
    total = int(totals[0].text) + int(totals[1].text)
    
    """