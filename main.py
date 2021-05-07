import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymssql

# conn = pymssql.connect(
#     server="10.175.1.60:1433",
#     user="importer_doc",
#     password='QAZxsw123',
#     database="Test")
#
# db = conn.cursor()

GLOBAL_URL = 'https://k2.com.pl'


proxy_lst = ['188.166.125.206:35145', '159.65.43.120:8080',
             '132.248.196.2:8080', '167.172.37.26:8080', '143.198.237.1:8080',
             '162.255.201.37:8080', '188.166.168.240:8080', '35.72.9.225:80',
             '167.172.37.26:8080', '219.92.3.149:8080', '164.90.164.161:8080',
             '188.240.71.213:3128', '203.74.120.79:3128', '167.99.54.28:8080'
             ]
# url = 'https://api.myip.com/'



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


def parsing():


    items_list = open("items_url.txt", "r")
    items_set = set(items_list.readlines())

    for item in list(items_set):
        if item.strip() != "https://k2.com.pl/produkty/w222-niska-sila-50-g":
            html_content = get_html(item.strip(), proxy_lst)
            soup = BeautifulSoup(html_content, "html.parser")
            item_file = open('item_file.txt', "a+")
            name = soup.find(class_="col-md-8 product-images").find("h1").get_text().strip()

            description = soup.find(id="opis").get_text()
            shot_descript = soup.find(class_="description-short").get_text()
            desct = shot_descript + description
            all_discript = desct.replace("\n", ' ').replace("'", '')
            numbers = soup.find(class_="product-index").get_text().strip().split("\n")
            index = numbers[0].split(":")[1].strip()
            barcode = numbers[1].split(":")[1].strip()
            item_file.write(index + "|" + barcode + "|" + name + "|" + item.strip() + "|" + all_discript +"\n")
            item_file.close()
            # # db.execute(f"INSERT INTO {schema_name}.items (vendor_code, name, item_url, barcode, discript) VALUES (N'{index}', N'{name}', N'{item.strip()}', N'{barcode}', N'{all_discript}')")
            # # conn.commit()
            #
            images = soup.find(class_="product-image").find_all("a")
            photo_file = open('photos.csv', "a+")
            for img in images:
                photo = img.get("href")

            #     photo_file.write(index + "|" + barcode + "|" + photo + "\n")
            photo_file.close()
            #     # db.execute(f"INSERT INTO {schema_name}.photos ("
            #     #            f"vendor_code,photo) VALUES (N'{index}', N'{photo}')")
            #     # conn.commit()
        else:
            pass


def creating():
    db.execute(f"CREATE SCHEMA {schema_name}")
    conn.commit()
#
    db.execute(f"CREATE TABLE {schema_name}.items (id int IDENTITY(1,1), "
               f"vendor_code NVARCHAR(230), "
               f"name NVARCHAR(355), "
               f"item_url NVARCHAR(330),"
               f"barcode NVARCHAR(330), "
               f"discript ntext)")
    conn.commit()

    db.execute(f"CREATE TABLE {schema_name}.photos (id int IDENTITY(1,1),  vendor_code NVARCHAR (130), photo NVARCHAR (330))")
    conn.commit()


if __name__ == '__main__':
    schema_name = "k2"
    # creating()
    # category()
    # product()
    parsing()







