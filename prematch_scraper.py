from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the ESPN Basketball Daily Lines webpage
url = "https://www.espn.com/nba/lines"

# Open the webpage
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Find the table containing line data
table = driver.find_element(By.XPATH, "//table[@class='Table__Table--align-right Table__Scroller__table']")
rows = table.find_elements(By.TAG_NAME, "tr")

# Iterate over rows to extract data
for row in rows:
    # Find all cells in the row
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0:
        # Extract data from cells
        team = cells[0].text
        spread = cells[1].text
        over_under = cells[2].text
        money_line = cells[3].text
        
        # Print the extracted data
        print("Team:", team)
        print("Spread:", spread)
        print("Over/Under:", over_under)
        print("Money Line:", money_line)
        print("-----------------------------")

# Close the browser
driver.quit()
