import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def scrape():

    # for news_title and news_p
    url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response_1 = requests.get(url_1)
    # Create BeautifulSoup object; parse with 'lxml'
    soup_1 = BeautifulSoup(response_1.text, 'lxml')

    results_1 = soup_1.find_all('div', class_="content_title")
    news_title = results_1[0].find('a').text

    results_2 = soup_1.find_all('div', class_="image_and_description_container")
    news_p = results_2[0].find('div', class_='rollover_description_inner').text

    # !which chromedriver

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_2)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # Retrieve page with the requests module
    response_img = requests.get(url_2)
    # Create BeautifulSoup object; parse with 'lxml'
    soup_img = BeautifulSoup(response_img.text, 'lxml')

    featured_image_url = soup_img.find('a', id="full_image")['data-fancybox-href']


    url_3 = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response_3 = requests.get(url_3)
    # Create BeautifulSoup object; parse with 'lxml'
    soup_3 = BeautifulSoup(response_3.text, 'lxml')


    results_3 = soup_3.find_all('p', class_='tweet-text')
    mars_weather_list = []
    for result in results_3:
        resultyy = result.text

        if resultyy[0:3] == "Sol":
            mars_weather_list.append(resultyy)
    #         print(resultyy)
    mars_weather = mars_weather_list[0]


    url_table = "https://space-facts.com/mars/"

    tables = pd.read_html(url_table)

    df = tables[0]
    df.columns = ['Diameters', 'Values']
    df.set_index("Diameters", inplace=True)

    hemisphere_image_urls = []

    url_dict = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    browser.visit(url_dict)

    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')

    browser.click_link_by_partial_text('Open')

    # Retrieve page with the requests module
    response_dict_1 = requests.get(url_dict)
    # Create BeautifulSoup object; parse with 'lxml'
    soup_dict_1 = BeautifulSoup(response_dict_1.text, 'lxml')

    dict_1 = {}
    results_dict_1 = soup_dict_1.find_all('img')
    img_url_1 = results_dict_1[1]['src']
    dict_1["title"] = "Cerberus Hemisphere"
    dict_1["img_url"] = img_url_1

    hemisphere_image_urls.append(dict_1)

    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')

    browser.click_link_by_partial_text('Open')

    dict_2 = {}
    results_dict_2 = soup_dict_1.find_all('img')
    img_url_2 = results_dict_2[4]['src']
    dict_2["title"] = "Valles Marineris Hemisphere"
    dict_2["img_url"] = img_url_2

    hemisphere_image_urls.append(dict_2)

    browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")

    browser.click_link_by_partial_text('Open')

    dict_3 = {}
    results_dict_3 = soup_dict_1.find_all('img')
    img_url_3 = results_dict_3[2]['src']
    dict_3["title"] = "Schiaparelli Hemisphere"
    dict_3["img_url"] = img_url_3

    hemisphere_image_urls.append(dict_3)

    browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")

    browser.click_link_by_partial_text('Open')

    dict_4 = {}
    results_dict_4 = soup_dict_1.find_all('img')
    img_url_4 = results_dict_4[3]['src']
    dict_4["title"] = "Syrtis Major Hemisphere"
    dict_4["img_url"] = img_url_4

    hemisphere_image_urls.append(dict_4)

    mars = {
        "last_news_title" : news_title,
        "last_news_p" : news_p,
        "image" : featured_image_url,
        "weather" : mars_weather,
        "info_table" : df.to_html(),
        "hemisphere" : hemisphere_image_urls
    }

    return mars
