import sqlite3
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import time




def scrape():
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # driver.get('https://www.imdb.com/')

    # time.sleep(5)
    # soup = BeautifulSoup(driver.page_source,'html.parser')
    # allNews = soup.find_all('div',class_="swiper-slide")

    # counter = 0
    news_list=[]

    # for news in allNews:

    #     title = news.find("div",class_="ipc-lockup-overlay sc-3148cda0-3 jSXLhI ipc-focusable").get("aria-label")
    #     images = news.find_all("img",class_="ipc-image")
    #     image_url = images[1].get("src")
        
    #     href = "https://www.imdb.com/"
    #     news_list.append([title,image_url,href])
    #     counter+=1
    #     if counter == 3:
    #         break




    driver.get('https://www.rottentomatoes.com')
    time.sleep(5)

    rottenTomatoes = BeautifulSoup(driver.page_source,'html.parser')
    r_news = rottenTomatoes.find_all('a',class_="article")

    counter=0
    for news in r_news:
        image_url = news.find("img").get("src")
        title = news.find("h2").text
        desc= news.find("p").text
        href = news.get("href")
        news_list.append([title,desc,image_url,href])
        counter+=1
        if counter == 7:
            break

    spotlights = []
    spotlights.append(rottenTomatoes.find("a",id="spotlight1"))
    spotlights.append(rottenTomatoes.find("a",id="spotlight2"))
    for tile in spotlights:
        image_url = tile.find("img").get("src")
        title = tile.find("h2").text
        desc = tile.find("p").text
        href = tile.get("href")
        news_list.append([title,desc,image_url,href])

    
    df = pd.DataFrame(news_list,columns=['title','desc','image_url','href'])
    


    conn = sqlite3.connect('Database/popcorn.db')
    df.to_sql('news', conn, if_exists='replace', index=True)
    conn.close()


if __name__ == "__main__":
    scrape()