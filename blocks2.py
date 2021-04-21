import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime
import time

proxy_lst = ['200.6.141.66:8080', '157.90.4.20:8001', '161.35.96.234:8080', '68.183.107.45:8080', '68.183.99.218:8080', '3.141.186.75:3128', '104.236.195.241:8080']
# # url = 'https://api.myip.com/'
# # url = 'https://www.myxa.com.ua/srs/get-ip/'
url = 'https://quotes.toscrape.com/'
#
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
#
#
# def pars():
#     urls_file = open("url2.txt")
#     urls = urls_file.readlines()
#     result_file = open("res.csv", "a+")
#
#     for urli in urls:
#         url = urli[:-1]
#         html = get_html(url, proxy_lst)
#         soup = BeautifulSoup(html, "html.parser")
#         quotes = soup.find_all(class_="quote")
#         for quote in quotes:
#             finder = quote.find(class_='text').get_text()
#
#             result_file.write(finder + "\n")
#
#     result_file.close()
#     urls_file.close()
#
#
if __name__ == '__main__':
    html = get_html(url, proxy_lst)
    f = open('xxx.txt', "w")
    f.write(html)
    f.close()
#     start = int(datetime.datetime.now().strftime("%H%M%S"))
#     pars()
#     stop = int(datetime.datetime.now().strftime("%H%M%S"))
#     print(f"Разница во  времени {stop - start} секунд")


