import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

from web_scraper.scrape_movie import scrape_from

driver = webdriver.Chrome()
driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')


last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    time.sleep(2)



soup = BeautifulSoup(driver.page_source,'html.parser')
allCards = soup.find_all('li',class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent")

movies =[]

for card in allCards:
    url = card.find("a").get("href")
    url = "https://www.imdb.com"+url
    movies.append(scrape_from(url))
    
    
columns = ['title', 'rating', 'image_url', 'desc', 'ott', 'ott_img','year','certificate','runtime','genre','directors', 'writers', 'stars']



df = pd.DataFrame(movies, columns=columns)
print(df)
df.to_csv('movie_details.csv', index=True)


conn = sqlite3.connect('Database/popcorn.db')
df.to_sql('movies', conn, if_exists='replace', index=True)
conn.close()