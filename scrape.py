
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import time

def init_browser():
    executable_path = {"'executable_path': '/usr/local/bin/chromedriver'"}
    return Browser('chrome', **executable_path, headless=False)

def scrape ():
    """Scrapes websites for information about Mars and returns information"""

    browser = init_browser()
    mars_data = {}


# # NASA Mars News

nasa_url = "https://mars.nasa.gov/news/"
response = requests.get(nasa_url)

soup = bs(response.text, 'html.parser')

print(soup.prettify())

soup.title.text

title = soup.find(class_='content_title').text
first_par = soup.find(class_='rollover_description_inner').text

print(f'Title:{title}')
print(f'First Paragraph:{first_par}')

# # JPL Mars Space Images - Featured Image

get_ipython().system('which chromedriver')

jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)
time.sleep(1)
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(1)
expand = browser.find_by_css('a.fancybox-expand')
expand.click()
time.sleep(1)

jpl_html = browser.html
jpl_soup = bs(jpl_html, 'html.parser')

img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
image_path = f'https://www.jpl.nasa.gov{img_relative}'
print(image_path)


# # Mars Weather

#* Visit the Mars Weather twitter account (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# Example:
#mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55

twitter_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter_url)
time.sleep(1)
twitter_url = browser.html
weather_soup = bs(twitter_url, 'html.parser')

tweets = weather_soup.find('ol', class_='stream-items')
mars_weather = tweets.find('p', class_="tweet-text").text
print(f'Mars Weather: {mars_weather}')


# # Mars Facts

#Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#Use Pandas to convert the data to a HTML table string.

facts_url = 'https://space-facts.com/mars/'
browser.visit(facts_url)
time.sleep(1)
facts_html = browser.html
facts_soup = bs(facts_html, 'html.parser')

fact_table = facts_soup.find('table', class_='tablepress tablepress-id-mars')
column1 = fact_table.find_all('td', class_='column-1')
column2 = fact_table.find_all('td', class_='column-2')

characteristics = []
values = []

for row in column1:
    characteristic = row.text.strip()
    characteristics.append(characteristic)

for row in column2:
    value = row.text.strip()
    values.append(value)

mars_facts = pd.DataFrame({
    "Characteristic":characteristics,
    "Value":values
    })

facts_html = mars_facts.to_html(header=False, index=False)
mars_facts


# # Mars Hemispheres

hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
hemisphere_image_urls = []

for i in range(1,9,2):
    hemisphere_dict = {}

    browser.visit(hemisphere_url)
    time.sleep(1)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    hemisphere_name_links = hemispheres_soup.find_all('a', class_='product-item')
    hemisphere_name = hemisphere_name_links[i].text.strip('Enhanced')

    detail_links = browser.find_by_css('a.product-item')
    detail_links[i].click()
    time.sleep(1)
    browser.find_link_by_text('Sample').first.click()
    time.sleep(1)
    browser.windows.current = browser.windows[-1]
    hemisphere_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()

    hemisphere_img_soup = bs(hemisphere_img_html, 'html.parser')
    hemisphere_img_path = hemisphere_img_soup.find('img')['src']

    print(hemisphere_name)
    hemisphere_dict['title'] = hemisphere_name.strip()

    print(hemisphere_img_path)
    hemisphere_dict['img_url'] = hemisphere_img_path

    hemisphere_image_urls.append(hemisphere_dict)

browser.quit()

hemisphere__image_urls
