from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import warnings
import arrow
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

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

original_totals = pd.DataFrame(columns = ["Team1", "Team2", "Original_Total", "Date"])

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0:
        team1 = cells[1].text.split(" ")
        team2 = cells[3].text.split(" ")
        Original_Total = float(cells[4].text)
        new_row = {"Team1": team1[-1] if len(team1) == 1 else team2[-1], "Team2": team1[-1] if len(team1) == 2 else team2[-1], "Original_Total": Original_Total, "Date": arrow.get(cells[0].text.split(",")[1].strip(), "MMMM D").format('MM-DD')}
        original_totals = original_totals.append(new_row, ignore_index = True) 
        

original_totals.to_csv("Prematch_Totals.csv", index = False)


driver.quit()
