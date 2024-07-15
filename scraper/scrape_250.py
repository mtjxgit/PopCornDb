"""
This script scrapes the top 250 movies from IMDb and saves the data
into a CSV file and a SQLite database.
"""

import sqlite3
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import movie

# Initialize the Chrome driver
driver = webdriver.Chrome()
driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')

# Scroll to the bottom of the page to load all content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    time.sleep(2)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
all_cards = soup.find_all(
    'li', class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent")

# Extract movie details
movies = []
for card in all_cards:
    url = card.find("a").get("href")
    url = "https://www.imdb.com" + url
    movies.append(movie.scrape_from(url))

# Create a DataFrame and save it to CSV
columns = ['title', 'rating', 'image_url', 'desc', 'ott', 'ott_img', 'year',
           'certificate', 'runtime', 'genre', 'directors', 'writers', 'stars']
df = pd.DataFrame(movies, columns=columns)
print(df)
df.to_csv('movie_details.csv', index=True)

# Save the DataFrame to a SQLite database
conn = sqlite3.connect('app/database/popcorn.db')
df.to_sql('movies', conn, if_exists='replace', index=True)
conn.close()

# Close the driver
driver.quit()
