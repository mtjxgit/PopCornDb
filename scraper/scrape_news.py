"""
Module to scrape news from Rotten Tomatoes and store them in a SQLite database.
"""

import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

# pylint: disable=R0914

def scrape():
    """
    Scrapes news articles from Rotten Tomatoes website and stores them in a SQLite database.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.rottentomatoes.com')
    time.sleep(5)

    news_list=[]
    rotten_tomatoes = BeautifulSoup(driver.page_source,'html.parser')
    r_news = rotten_tomatoes.find_all('a',class_="article")

    
    for news in r_news:
        image_url = news.find("img").get("src")
        title = news.find("h2").text
        desc = news.find("p").text
        href = news.get("href")
        news_list.append([title, desc, image_url, href])
        

    spotlights = []
    spotlights.append(rotten_tomatoes.find("a", id="spotlight1"))
    spotlights.append(rotten_tomatoes.find("a", id="spotlight2"))
    for tile in spotlights:
        image_url = tile.find("img").get("src")
        title = tile.find("h2").text
        desc = tile.find("p").text
        href = tile.get("href")
        news_list.append([title, desc, image_url, href])

    df = pd.DataFrame(news_list, columns=['title', 'desc', 'image_url', 'href'])

    conn = sqlite3.connect('app/database/popcorn.db')
    df.to_sql('news', conn, if_exists='replace', index=True)
    conn.close()

if __name__ == "__main__":
    scrape()
