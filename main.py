import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymssql
import psycopg2
import time
import os

# conn = pymssql.connect(
#     server="10.175.1.60:1433",
#     user="importer_doc",
#     password='QAZxsw123',
#     database="Test")
#
# db = conn.cursor()
conn = psycopg2.connect(
    host='localhost',
    user='step',
    password='Stomatolog',
    database='yana_db')

db = conn.cursor()
GLOBAL_URL = 'https://k2.com.pl'


# # proxy_lst = ['142.44.136.219:32768', '167.99.54.28:8080', '150.136.5.47:80', '167.99.126.178:8080',
# #              '167.99.59.236:8080', '18.223.113.144:3128', '167.99.112.188:8080', '162.255.201.37:8080',
# #              '51.222.67.219:32768', '198.50.163.192:3129', '178.62.127.204:8080', '104.131.59.152:8080',
# #              '178.62.61.32:8080', '188.240.71.213:3128', '52.143.81.17:3128', '51.158.123.35:9999',
# #              '46.101.83.76:8080', '167.172.37.26:8080', '46.101.130.118:8080', '168.119.137.56:3128']
proxy_lst = []

def get_html(url, proxy_lst):
    ua = UserAgent()
    x = True

    while x:
        rand_ip = choice(proxy_lst)
        print(rand_ip)

        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome},
                               timeout=10)
        except:
            print("Try")
        else:
            x = False
            if req.status_code == 200:
                return req.content
            else:
                print(req.status_code)
                print("ERROR ", url)


def category():
    categories_lst = []
    content_html = get_html(main_url, proxy_lst)
    soup = BeautifulSoup(content_html, "html.parser")
    all_categories = soup.find(class_="category-list")
    for item in all_categories.select("ul.child-category-list"):
        item.decompose()
    categories_result = all_categories.find_all("li")
    for li in categories_result:
        link = li.find("a").get("href")
        if link[0] == '/':
            categories_lst.append(GLOBAL_URL + link)
        else:
            categories_lst.append(link)
    return categories_lst



def parsing_items_url(categories):
    file_items_urls = open("items_url.txt", "a+")
    for cat_url in categories[:-2]:
        html_product = get_html(cat_url, proxy_lst)
        cont_soup = BeautifulSoup(html_product, "html.parser")
        try:
            all_paginations = cont_soup.find(class_="pagination").find_all("li")
        except:
            print("NO pagination")
            products_no_pagination = cont_soup.find_all(class_="go-to-product")
            for prod_no_page in products_no_pagination:
                    item_pagefree = prod_no_page.get("href")
                    page_zero = GLOBAL_URL + item_pagefree
                    file_items_urls.write(page_zero + "\n")
        else:
            last_page = all_paginations[-1].find("a").get('href')
            page = last_page.split("=")[1]
            print("Pagination is ", page)
            for i in range(1, int(page)+1):
                pages_ulr = cat_url.strip() + "?page=" + str(i)
                cat_pagination = get_html(pages_ulr, proxy_lst)
                item_soup = BeautifulSoup(cat_pagination, "html.parser")
                products = item_soup.find_all(class_="go-to-product")
                for prod in products:
                    href_item = prod.get("href")
                    item_url = GLOBAL_URL + href_item
                    file_items_urls.write(item_url + "\n")


def cardos(cat_url):
    file_cardos = open('other_shop', "a+")
    cardos_URL = "http://cardos.com"
    cardos_html = get_html(cat_url, proxy_lst)
    cardos_soup = BeautifulSoup(cardos_html, "html.parser")
    category_cardos = cardos_soup.find(class_="catid-120").find("a").get("href")
    cardos_link = cardos_URL + category_cardos

    html_pagination = get_html(cardos_link, proxy_lst)
    pagination_soup = BeautifulSoup(html_pagination, "html.parser")
    max_pagination = pagination_soup.find(class_="pagination").find_all("a")[-1].get("href").split("=")[1]

    for i in range(1, int(max_pagination) + 1):
        link_with_pagination = cardos_link + "?page=" + str(i)
        cardos_items = get_html(link_with_pagination, proxy_lst)
        items_soup = BeautifulSoup(cardos_items, "html.parser")
        all_blocks = items_soup.find_all(class_="block")
        for block in all_blocks:
            item_url = block.find("a").get("href")
            file_cardos.write(cardos_URL + item_url + '\n')
    file_cardos.close()
    file_card = open('other_shop', 'r')
    cardos_lst = file_card.readlines()

    for el in cardos_lst:
        time.sleep(16)

        print(el.strip())
        product_html = get_html(el.strip(), proxy_lst)
        soup = BeautifulSoup(product_html, "html.parser")
        name = soup.find(class_="product-page").find(class_="title").get_text()
        if soup.find(class_="product-page").find(class_="description-short"):
            shot_descript = soup.find(class_="product-page").find(class_="description-short").get_text()
        else:
            shot_descript = ''
        index = soup.find(class_="reference").get_text().split(":")[1].strip()
        barcode = soup.find(class_="ean").get_text().split(":")[1].strip()
        long_description = soup.find(class_="content").get_text()
        common_descript = (shot_descript + long_description).replace("\n", ' ')
        db.execute(
            f"INSERT INTO {schema_name}.items (vendor_code, barcode, name, item_url, discript) VALUES (N'{index}', N'{barcode}', N'{name}', N'{el.strip()}', N'{common_descript}')")
        conn.commit()

        imgs = soup.find(class_="previews").find_all('a')
        for photo_href in imgs:
            photo = photo_href.get("href")
            db.execute(f"INSERT INTO {schema_name}.photos (vendor_code, barcode, photo) VALUES (N'{index}', N'{barcode}', N'{photo}')")
            conn.commit()
    os.remove("/home/yevhen7/Documents/yana/k2/k2/other_shop")

def masner(cat_url):

    file_cardos = open('other_shop', "a+")
    main_URL = "http://masner.com"
    cardos_html = get_html(cat_url, proxy_lst)
    cardos_soup = BeautifulSoup(cardos_html, "html.parser")
    category_cardos = cardos_soup.find(class_="catid-120").find("a").get("href")

    cardos_link = main_URL + category_cardos
    html_pagination = get_html(cardos_link, proxy_lst)
    if html_pagination != None:
        pagination_soup = BeautifulSoup(html_pagination, "html.parser")
        max_pagination = pagination_soup.find(class_="pagination").find_all("a")[-1].get("href").split("=")[1]
        print(max_pagination)
        for i in range(1, int(max_pagination) + 1):
            link_with_pagination = cardos_link + "?page=" + str(i)
            cardos_items = get_html(link_with_pagination, proxy_lst)
            items_soup = BeautifulSoup(cardos_items, "html.parser")
            all_blocks = items_soup.find_all(class_="block")
            for block in all_blocks:
                item_url = block.find("a").get("href")
                file_cardos.write(main_URL + item_url + '\n')
        file_cardos.close()
    else:
        print("error")
    file_card = open('other_shop', 'r')
    cardos_lst = file_card.readlines()

    for el in cardos_lst:

        print(el.strip())
        product_html = get_html(el.strip(), proxy_lst)
        soup = BeautifulSoup(product_html, "html.parser")
        product = soup.find(class_="product-page")
        if product:
            name = soup.find(class_="product-page").find(class_="title").get_text()
            if soup.find(class_="product-page").find(class_="description-short"):
                shot_descript = soup.find(class_="product-page").find(class_="description-short").get_text()
            else:
                shot_descript = ''

            index = soup.find(class_="reference").get_text().split(":")[1].strip()

            barcode = soup.find(class_="ean").get_text().split(":")[1].strip()

            long_description = soup.find(class_="content").get_text()

            common_descript = (shot_descript + long_description).replace("\n", ' ')
            db.execute(
                f"INSERT INTO {schema_name}.items (vendor_code, name, item_url, barcode, discript) VALUES (N'{index}', N'{name}', N'{el.strip()}', N'{barcode}', N'{common_descript}')")
            conn.commit()

            imgs = soup.find(class_="previews").find_all('a')
            for photo_href in imgs:
                photo = photo_href.get("href")

                db.execute(f"INSERT INTO {schema_name}.photos ("
                           f"vendor_code, barcode, photo) VALUES (N'{index}', N'{barcode}', N'{photo}')")
                conn.commit()

        else:
            print("product is out in stock ", el)
    os.remove("/home/yevhen7/Documents/yana/k2/k2/other_shop")


def parsing_other_shops(categories):
    for cat_url in categories:

        if cat_url == 'http://cardos.com/produkty':
            cardos(cat_url)

        if cat_url.strip() == 'http://masner.com/produkty':
            masner(cat_url)


def parsing_product_k2():
    items_list = open("items_url.txt", "r")
    items_set = set(items_list.readlines())

    for item in list(items_set):
        print(item.strip())
        if item.strip() != "https://k2.com.pl/produkty/w222-niska-sila-50-g":
            html_content = get_html(item.strip(), proxy_lst)
            soup = BeautifulSoup(html_content, "html.parser")
            name = soup.find(class_="col-md-8 product-images").find("h1").get_text().strip()
            description = soup.find(id="opis").get_text()
            shot_descript = soup.find(class_="description-short").get_text()
            desct = shot_descript + description
            all_discript = desct.replace("\n", ' ').replace("'", '')
            numbers = soup.find(class_="product-index").get_text().strip().split("\n")
            index = numbers[0].split(":")[1].strip()
            barcode = numbers[1].split(":")[1].strip()

            db.execute(f"INSERT INTO {schema_name}.items (vendor_code, barcode, name, item_url, discript) VALUES (N'{index}', N'{barcode}', N'{name}', N'{item.strip()}', N'{all_discript}')")
            conn.commit()

            images = soup.find(class_="product-image").find_all("a")
            for img in images:
                photo = img.get("href")
                db.execute(f"INSERT INTO {schema_name}.photos ("
                           f"vendor_code,barcode, photo) VALUES (N'{index}', N'{barcode}',N'{photo}')")
                conn.commit()
        else:
            pass


def creating():
    db.execute(f"CREATE SCHEMA {schema_name}")
    conn.commit()

    db.execute(f"create table {schema_name}.items (id SERIAL , "
               f"vendor_code nchar(230), "
               f"barcode nchar(330), "
               f"name nchar(355), "
               f"item_url nchar(330),"
               f"discript text)")
    conn.commit()

    db.execute(f"CREATE TABLE {schema_name}.photos (id  SERIAL,  "
               f"vendor_code nchar (130), "
               f"barcode nchar (130), "
               f"photo nchar (330))")
    conn.commit()


if __name__ == '__main__':
    main_url = "https://k2.com.pl/produkty"
    schema_name = "k2"
    creating()
    categories = category()
    parsing_items_url(categories)
    parsing_product_k2()
    parsing_other_shops(categories)








