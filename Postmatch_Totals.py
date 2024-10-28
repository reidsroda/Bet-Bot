import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#Data Storage
conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()
df = pd.DataFrame(columns = ['team1', 'team1_Q1','team1_Q2', 'team1_Q3', 'team1_Q4', 'team2', 'team2_Q1', 'team2_Q2', 'team2_Q3', 'team2_Q4', 'Total'])

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
                    date DATE )
                    ''')
                   

conn.commit()


# Function to get yesterday's date
"""
def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime('%Y-%m-%d')
    """


# Scrape NBA game results from ESPN or NBA.com
def scrape_nba_results():
    
    driver = webdriver.Chrome()
    driver.get("https://www.espn.com/nba/scoreboard/_/date/20241023")
    driver.maximize_window()

    
    # Wait for the page to load
    time.sleep(15)
    
    global df
   
    # Get all game containers (customize the selector based on the page structure)
    games = driver.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell__Competitors')
    for game in games:
        try:
            # Team names
            teams = game.find_elements(By.CLASS_NAME, 'ScoreCell__TeamName')
            team_1 = teams[0].text
            team_2 = teams[1].text

            # Scores
            scores = game.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell__Value')
            team_1_q1 = int(scores[0].text)
            team_1_q2 = int(scores[1].text)
            team_1_q3 = int(scores[2].text)
            team_1_q4 = int(scores[3].text)
            team_2_q1 = int(scores[4].text)
            team_2_q2 = int(scores[5].text)
            team_2_q3 = int(scores[6].text)
            team_2_q4 = int(scores[7].text)
            total = team_1_q1 + team_1_q2 + team_1_q3 + team_1_q4 + team_2_q1 + team_2_q2 + team_2_q3 + team_2_q4
            todays_date = datetime.now().strftime('%Y-%m-%d')

            # Append the result to the list
            #new_row = {'team1': team_1, 'team1_Q1': team_1_q1,'team1_Q2': team_1_q2, 'team1_Q3': team_1_q3, 'team1_Q4': team_1_q4, 'team2': team_2, 'team2_Q1':team_2_q1, 'team2_Q2': team_2_q2, 'team2_Q3': team_2_q3, 'team2_Q4': team_2_q4, 'Total': total}
            #df = df.append(new_row, ignore_index = True)
            
            
            
            conn.commit()
            
        except Exception as e:
            print(f"Error processing game data: {e}")
            
        new_row = (team_1, team_1_q1, team_1_q2, team_1_q3, team_1_q4, team_2, team_2_q1, team_2_q2, team_2_q3, team_2_q4, total, todays_date)
        cursor.execute("INSERT INTO postmatch_totals (team1, team1_Q1, team1_Q2, team1_Q3, team1_Q4, team2, team2_Q1, team2_Q2, team2_Q3, team2_Q4, Total, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", new_row)
        conn.commit()
            

    cursor.close()
    conn.close()
    driver.quit()



scrape_nba_results()


