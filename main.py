import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime
import time

GLOBAL_URL = 'https://k2.com.pl'


proxy_lst = ['177.229.130.68:8080', '45.70.197.222:999', '168.119.137.56:3128','167.172.37.26:8080',
             '143.198.56.222:8888', '207.154.254.25:8080', '20.71.134.39:8080', '132.248.196.2:8080',
             '188.166.111.50:3128', '143.198.237.1:8080', '40.85.152.26:8080', '64.225.8.192:80', '162.255.201.37:8080',
             '165.227.229.14:8080', '149.28.94.152:8080', '188.166.210.52:8080', '162.255.201.37:8080',
             '178.128.242.151:8080', '188.166.168.240:8080', '35.72.9.225:80', '141.226.18.206:8080',
             '167.172.191.249:34951', '93.157.251.134:3128', '42.117.228.47:80', '194.250.57.253:8080',
             '167.172.191.249:34584', '143.198.237.1:8080']
# url = 'https://api.myip.com/'
# url = 'https://www.myxa.com.ua/srs/get-ip/'



def get_html(url, proxy_lst):
    ua = UserAgent()
    x = True

    while x:
        rand_ip = choice(proxy_lst)
        print(rand_ip)
        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
        except:
            print("Try")
        else:
            x = False
            print(req.status_code)
            return req.text


def category():

    url = "https://k2.com.pl/produkty"
    html = get_html(url, proxy_lst)

    soup = BeautifulSoup(html, "html.parser")
    finders = soup.find_previous(class_="fa fa-arrow-down")
    print(finders)
    # for finder in finders:
    #     url = finder.find("a").get("href")
    #     print(url)
    # for finder in finders:
    #     url = finder.find("a").get('href')
    #
    #     urls_file = open('categories.txt', "a+")
    #     urls_file.write(GLOBAL_URL + url + '\n')
    #     urls_file.close()


def product():
    urls = open('categories.txt', "r")
    category_url = urls.readlines()


    for cat_url in category_url[:-2]:
        print(cat_url.strip())
        html_product = get_html(cat_url.strip(), proxy_lst)
        cont_soup = BeautifulSoup(html_product, "html.parser")
        urls_file = open('items_url.txt', "a+")
        try:
            all_paginations = cont_soup.find(class_="pagination").find_all("li")
        except:
            print("NO pagination")
            products_no_pagination = cont_soup.find_all(class_="go-to-product")
            for prod_no_page in products_no_pagination:
                    item_pagefree = prod_no_page.get("href")
                    page_zero = GLOBAL_URL + item_pagefree
                    urls_file.write(page_zero + "\n")
        else:
            last_page = all_paginations[-1].find("a").get('href')
            page = last_page.split("=")[1]
            print("Pagination is ", page)

            for i in range(1, int(page)+1):
                pages_ulr = cat_url.strip() + "?page=" + str(i)
                items_url = get_html(pages_ulr, proxy_lst)
                item_soup = BeautifulSoup(items_url, "html.parser")
                products = item_soup.find_all(class_="go-to-product")

                for prod in products:
                    href_item = prod.get("href")
                    item_url = GLOBAL_URL + href_item
                    urls_file.write(item_url + "\n")

        urls_file.close()



# _____________________________________________________________________________________________
if __name__ == '__main__':
    # category()
    product()








