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

with open('../data/index','rb') as f:
    index_list = pickle.load(f)

links_list_missing = []
for ind in index_list:
    link = links_list[ind]
    links_list_missing.append(link)

urls = []
for l in links_list_missing[1:]:
    url = l[1]
    urls.append(url)

missing_l = []
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
for l in urls:
    page = l
    PageTree = requests.get(page, headers=headers)
    soup = BeautifulSoup(PageTree.content, 'html.parser')
    new_loc = soup.find('a',{'class': 'trail-rank-link'})
    if new_loc:
        loc = new_loc.get_text()
    else:
        loc = 'None'
    missing_l.append(loc)


with open('../data/mis_loc', 'wb') as fp:
    pickle.dump(missing_l, fp)
