import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


def movie_scrape():
    driver = webdriver.Chrome()
    driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')

    detailed_view_button = driver.find_element("xpath", '//button[@id="list-view-option-detailed"]')
    detailed_view_button.click()
    time.sleep(2)

    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(scroll_pause_time)



    soup = BeautifulSoup(driver.page_source,'html.parser')
    allCards = soup.find_all('li',class_="ipc-metadata-list-summary-item")

    movies =[]
    for card in allCards:
        image_url = card.find('img',class_="ipc-image").get('src')
        
        title = card.find('h3',class_="ipc-title__text").text.split(".",1)[1].lstrip()
        
        allSpan = card.find_all('span',class_="sc-b189961a-8 kLaxqf dli-title-metadata-item")
        
        details = []
        for i in allSpan:
            details.append(i.text)
        year = details[0]
        runtime = details[1]
        certificate = details[2]
        rating = card.find('span',class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text [0:3]

        desc = card.find("div",class_="ipc-html-content-inner-div").text

        allCrew = card.find_all("span",class_="sc-74bf520e-5 ePoirh")
        crew=[]
        for span in allCrew:
            crew.append(span.text)
        director = crew[0]
        star1 = crew[1]
        star2 = crew[2]
        star3 = crew[3]

        

        movies.append([rating,image_url,title,desc,director,year,runtime,certificate,star1,star2,star3])
        
    df = pd.DataFrame(movies,columns=['rating','image_url','title','desc','director','year','runtime','certificate','star1','star2','star3'])



    conn = sqlite3.connect('Database/popcorn.db')
    df.to_sql('movies', conn, if_exists='replace', index=True)
    conn.close()


if __name__ == "__main__":
    movie_scrape()