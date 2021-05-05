import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime
import time



with open("cont.html", "r") as file:
    file_wr = open("categories.txt", "a+")
    text = file.read()
    soup = BeautifulSoup(text, "html.parser")
    finders = soup.find(class_="category-list")
    for item in finders.select("ul.child-category-list"):
        item.decompose()
    s = finders.find_all("li")
    for li in s:
        link = li.find("a").get("href")
        file_wr.write("https://k2.com.pl/" + link + '\n')
    file_wr.close()













# ___________________________________________________________________________________
# item parsing
# with open("cont.html", "r") as file:
#     text = file.read()
#     soup = BeautifulSoup(text, "html.parser")
#     name = soup.find(class_="col-md-8 product-images").find("h1").get_text().strip()
#
#     # description = soup.find(class_="description").get_text()
#     description = soup.find(id="opis").get_text()
#     shot_descript = soup.find(class_="description-short").get_text()
#     desct = shot_descript + description
#     d = desct.replace("\n", ' ')
#     print(d)
#     numbers = soup.find(class_="product-index").get_text().strip().split("\n")
#     index = numbers[0].split(":")[1].strip()
#     barcode = numbers[1].split(":")[1].strip()
#
#     images = soup.find(class_="product-image").find_all("a")
#     for img in images:
#         photo = img.get("href")
#         #TODO  conect with index
# _______________________________________________________________________________________