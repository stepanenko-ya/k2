import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime
import time


proxy_lst = ['188.166.125.206:35145', '159.65.43.120:8080',
             '132.248.196.2:8080', '167.172.37.26:8080', '143.198.237.1:8080',
             '162.255.201.37:8080', '188.166.168.240:8080', '35.72.9.225:80',
             '167.172.37.26:8080', '219.92.3.149:8080', '164.90.164.161:8080',
             '188.240.71.213:3128', '203.74.120.79:3128', '167.99.54.28:8080'
             ]
def get_html(url, proxy_lst):
    ua = UserAgent()
    x = True

    while x:
        rand_ip = choice(proxy_lst)
        print(rand_ip)
        print(url)
        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
        except:
            print("Try")
        else:
            x = False
            print(req.status_code)

            return req.text







def main():
    # get_html("http://cardos.com/produkty/wedlug-serii", proxy_lst)
    file = open("content.txt", "r")
    f = file.read()
    soup = BeautifulSoup(f, "html.parser")
    name = soup.find(class_="product-page").find(class_="title").get_text()
    shot_descript = soup.find(class_="product-page").find(class_="description-short").get_text()
    index = soup.find(class_="reference").get_text().split(":")[1].strip()
    barcode = soup.find(class_="ean").get_text().split(":")[1].strip()
    long_description = soup.find(class_="content").get_text()
    common_descript = (shot_descript + long_description).replace("\n", ' ')

    imgs = soup.find(class_="previews").find_all('a')
    for photo_href in imgs:
        photo = photo_href.get("href")



main()