import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    # html object
    html = browser.html

    # parse html with BS
    soup = BeautifulSoup(html, 'html.parser')

    # Retrive latest news Title and Paragraph text.
    news_title = soup.find(class_='content_title').find('a').text
    news_paragraph = soup.find(class_='article_teaser_body').text
    time.sleep(2)

    # ## Mars Featured Image

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)
    # Got to full image
    browser.click_link_by_id('full_image')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    # html object
    html_image = browser.html

    # parse html with BS
    img_soup = BeautifulSoup(html_image, 'html.parser')

    # Retrive latest news Title and Paragraph text.
    full_image_url = img_soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov'+full_image_url
    # featured_image_url

    # ## Mars Weather - Twitter

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)

    # html object
    html_weather = browser.html

    # parse html with BS
    weather_soup = BeautifulSoup(html_weather, 'html.parser')

    # Highest level container for individual tweets
    weather_tweet = weather_soup.find_all(
        'div', class_='js-tweet-text-container')

    # Look for weather related tweets only
    for tweet in weather_tweet:
        mars_weather = tweet.find('p', class_='TweetTextSize').text
        if 'InSight sol' in mars_weather:
            print(mars_weather)
            break

    # ## Mars Facts

    facts_url = 'https://space-facts.com/mars/'

    # Use Pandas read_html to parse the url
    tables = pd.read_html(facts_url)

    # Choose correct table
    access_table = tables[1]
    # Rename column names
    access_table.columns = ['Facts', 'Value']
    access_table

    # add a htmlfile name inside of the brackets and it
    mars_facts_html = access_table.to_html(buf=None)
    # pprint(mars_facts_html)

    # browser.quit()
    # return mars_facts_html

    # ## Mars Hemis

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(2)

    html_hemispheres = browser.html

    hemispheres_soup = BeautifulSoup(html_hemispheres, 'html.parser')

    info = hemispheres_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for items in info:

        # title page
        title = items.find('h3').text

        # partial image link
        image_url = items.find('a', class_='itemLink product-item')['href']
        # getting full image link
        full_image_url = 'https://astrogeology.usgs.gov'+image_url
        browser.visit(full_image_url)
        time.sleep(2)

        size_url = browser.html
        soup = BeautifulSoup(size_url, 'html.parser')
        img_url = 'https://astrogeology.usgs.gov' + \
            soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    hemisphere_image_urls

    mars_info = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_info
