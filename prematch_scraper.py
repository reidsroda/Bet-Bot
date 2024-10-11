#ONLY RUN THIS CODE ONCE PER DAY
#IN FUTURE AUTOMATE IT TO RUN AT SPECIFIC TIME EACH DAY


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import warnings
import arrow
import warnings
import sqlite3

warnings.simplefilter(action='ignore', category=FutureWarning)

#Data Storage
conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS prematch_totals (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    team1 TEXT,
                    team2 TEXT,
                    original_total DECIMAL,
                    date DATE) ''')

conn.commit()


# Setting up Chrome WebDriver
driver = webdriver.Chrome()
driver.get("https://bettingdata.com/nba/over-under")
driver.maximize_window()

# Wait for the page to load
time.sleep(15)
driver.find_element(By.XPATH ,"/html/body/div[6]/div/div[4]/div/div/div/div/div/section/div/div[2]/div/div/a[2]").click()
time.sleep(15)
table = driver.find_element(By.XPATH, "//*[@id='stats_grid']/div[2]/table/tbody")
rows = table.find_elements(By.TAG_NAME, 'tr')


#Scrape All Prematch Total Lines
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0:
        team1_t = cells[1].text.split(" ")
        team2_t = cells[3].text.split(" ")
        Date_month_day = cells[0].text.split(",")[1].strip()
        Date_year = cells[0].text.split(",")[2].strip()[:4]
        Date = arrow.get(Date_month_day + " " + Date_year, "MMMM D YYYY").format('MM-DD-YYYY')
        team1 = team1_t[-1] if len(team1_t) == 1 else team2_t[-1]
        team2 = team1_t[-1] if len(team1_t) == 2 else team2_t[-1]
        try: 
            Original_Total = float(cells[4].text)
            new_row = (team1, team2, Original_Total, Date)
            cursor.execute("INSERT INTO prematch_totals (team1, team2, original_total, date) values (?, ?, ?, ?)", new_row)
            conn.commit()
        except ValueError:
            continue
        
        
        
cursor.close()
conn.close()
driver.quit()
