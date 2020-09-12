#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import os
import time

# url address
URL = "https://mothcub.tumblr.com/tagged/art"
# page count
page_no = 1
# the most recent saved image
RECENT = sorted(["178038585699"] + os.listdir("art/"))[-1]
# big img id, should work for the next few years
img_id = "9"*20

while img_id > RECENT:
    # crawl source
    page_source = urllib.request.urlopen(URL+"/page/"+str(page_no))
    page_html = page_source.read().decode('utf-8')
    page = BeautifulSoup(page_html, 'html.parser')

    # pretend you're a real person
    time.sleep(3)

    # scrap the images
    arts = page.findAll("div", {"class": "photo"})
    for art in arts:
        img_id = art.img.parent["href"].split('/')[-1]
        urllib.request.urlretrieve(
            art.img["src"], "art/" + img_id)
        if img_id == RECENT:
            break
    page_no += 1
    print('#', end='')    
    