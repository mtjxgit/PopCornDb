"""
This module contains the function scrape_from which scrapes movie details from a given IMDb URL.
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
# pylint: disable=line-too-long
# pylint: disable=R0914

def scrape_from(url):
    """
    Scrape movie details from the given IMDb URL.

    Args:
        url (str): The IMDb URL of the movie to scrape.

    Returns:
        list: A list containing movie details such as title, image URL, rating, genre, description, 
              year, certificate, runtime, OTT platform, OTT image, directors, writers, and stars.
    """
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = soup.find("span", class_="hero__primary-text").text
    image_url = soup.find("img", class_="ipc-image").get("src")
    rating = soup.find("span", class_="sc-eb51e184-1 cxhhrI").text

    genre = ', '.join(tag.text for tag in soup.find_all("span", class_="ipc-chip__text"))

    desc_element = soup.find("span", class_="sc-2d37a7c7-1 eSoBYy")
    desc = desc_element.text if desc_element else ''

    ul = soup.find("ul",
                   class_=
                   "ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt")
    li_elements = ul.find_all('li')
    year, certificate, runtime = [li.text.strip() if li else "" for li in li_elements[:3]]

    ott_element = soup.find("div", class_="sc-525759fc-1 hNXzIr")
    streaming = soup.find("div", class_="sc-805604aa-0 bweHYD")
    if ott_element and "STREAMING" in streaming.text:
        ott_img = ott_element.find("img").get("src")
        ott = ott_element.find("img").get("alt")[9:] if ott_element.find("img") else ''
    else:
        ott_img = ''
        ott = ''

    all_li = soup.find_all("li", class_="ipc-metadata-list__item")

    directors_element = all_li[0] if len(all_li) > 0 else None
    directors = ', '.join(a.text for a in directors_element
                          .find_all("a",
                                    class_=
                                    "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"
    )) if directors_element else ''

    writers_element = all_li[1] if len(all_li) > 1 else None
    writers = ', '.join(a.text for a in writers_element
                        .find_all("a",
                                  class_=
                                  "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"
    )) if writers_element else ''

    stars_element = all_li[2] if len(all_li) > 2 else None
    stars = ', '.join(a.text for a in stars_element.find_all(
        "a",
        class_=
        "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"
    )) if stars_element else ''

    details = [
        title, image_url, rating, genre, desc, year, certificate, runtime, ott, ott_img, directors, writers, stars
    ]

    return details
