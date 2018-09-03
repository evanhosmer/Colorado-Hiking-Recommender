from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import requests
import pickle
import csv

# url = 'https://www.alltrails.com/us/colorado'
#
# driver = webdriver.Chrome(executable_path="/Users/evanhosmer/Downloads/chromedriver")
# driver.get(url)
# driver.implicitly_wait(30)

# selectElem = driver.find_element_by_xpath(//*[@id="load_more"])

def get_all_hikes(browser):
    '''
    INPUT: browser
    OUTPUT: soup object with all loaded hikes
    '''

    while True:
        try:
            load_more_hikes = driver.find_element_by_xpath("//div[@id='load_more'] [@class='feed-item load-more trail-load'][//a]")
            load_more_hikes.click()
            time.sleep(7)
        except:
            break
    soup = BeautifulSoup(browser.page_source, "html")

    return soup

def get_hike_links(soup):
    '''
    INPUT: soup object
    OUTPUT: links for all hikes
    '''

    li = soup.find_all('h3', {'class': 'name short'})
    links = []
    for Sub in li:
        links.append(Sub.find("a").get('href'))

    newlinks = []
    for l in links:
        newl = 'https://www.alltrails.com' + l
        newlinks.append(newl)

    return newlinks

def get_hike_data(links):
    '''
    INPUT: list of hike links
    OUTPUT: hike metadata for all hikes
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    rows = []
    for l in links:
        row = []
        page = l
        PageTree = requests.get(page, headers=headers)
        soup = BeautifulSoup(PageTree.content, 'html.parser')
        title = soup.find('h1', {'itemprop': 'name'}).get_text()
        difficulty = soup.find('div',{'id': 'difficulty-and-rating'}).findChildren()
        diff = difficulty[0].get_text()
        row.append(title)
        row.append(diff)
        vals = soup.find_all('div',{'class': 'detail-data'})
        for l in vals:
            row.append(l.get_text())
        feats = soup.find_all('span',{'class': 'big rounded active'})
        for f in feats:
            row.append(f.get_text())
        rows.append(row)

    return rows


# soup = get_all_hikes(driver)
# links = get_hike_links(soup)
with open('hiking-links.csv') as f:
   reader = csv.reader(f)
   links_list = list(reader)

urls = []
for l in links_list[1:]:
    url = l[1]
    urls.append(url)

data = get_hike_data(urls)

with open('outfile', 'wb') as fp:
    pickle.dump(data, fp)

# with open ('outfile', 'rb') as fp:
#     itemlist = pickle.load(fp)
