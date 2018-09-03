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

with open('../data/hiking-links.csv') as f:
   reader = csv.reader(f)
   links_list = list(reader)

urls = []
for l in links_list[1:]:
    url = l[1]
    urls.append(url)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
locations = []
stars = []

for l in urls:
    page = l
    PageTree = requests.get(page, headers=headers)
    soup = BeautifulSoup(PageTree.content, 'html.parser')
    loc = soup.find('span', {'itemprop': 'name'})
    if loc:
        location = loc.get_text()
    else:
        location = 'None'
    sta = soup.find('meta',{'itemprop': 'ratingValue'})
    if sta:
        star = sta.get('content')
    else:
        star = 'None'
    locations.append(location)
    stars.append(star)

with open('../data/locations', 'wb') as fp:
    pickle.dump(locations, fp)

with open('../data/stars', 'wb') as fp:
    pickle.dump(stars, fp)
