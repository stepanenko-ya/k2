import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime
import time

GLOBAL_URL = 'https://k2.com.pl'

proxy_lst = ['13.212.71.73:80', '78.110.7.192:3128', '132.145.18.53:80', '35.72.9.225:80', '178.33.148.10:3128', '14.192.31.17:50838',
             '200.6.141.66:8080', '157.90.4.20:8001', '161.35.96.234:8080', '68.183.107.45:8080', '68.183.99.218:8080', '3.141.186.75:3128', '104.236.195.241:8080']
# url = 'https://api.myip.com/'
# url = 'https://www.myxa.com.ua/srs/get-ip/'
# url = 'https://quotes.toscrape.com/'

def get_html(url, proxy_lst):
    ua = UserAgent()
    x = True
    while x:
        rand_ip = choice(proxy_lst)
        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        print(prox)
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=20)
        except:
            print("Try")
        else:
            x = False
            print(req.status_code)
            return req.text


def pars():

    url = "https://k2.com.pl/produkty"
    html = get_html(url, proxy_lst)

    soup = BeautifulSoup(html, "html.parser")
    finders = soup.find(class_="category-list").find_all("li")
    for finder in finders:
        url = finder.find("a").get('href')

        urls_file = open('categors_urls.txt', "a+")
        urls_file.write(GLOBAL_URL + url + '\n')
        urls_file.close()


def product(u):
    html_product = get_html(u, proxy_lst)
    soup = BeautifulSoup(html_product, "html.parser")
    item = soup.find(class_="")


if __name__ == '__main__':

    # pars()
    urls = open('categors_urls.txt', "r")
    u = urls.readline().strip()
    product(u)






