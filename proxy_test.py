import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymssql
import psycopg2
import time

conn_ms = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

conn = psycopg2.connect(
    host='localhost',
    user='stepanenko',
    password='Stomatolog',
    database='test2',)

db = conn.cursor()
db_ms = conn_ms.cursor()


def creating():

    db.execute("CREATE TABLE dbo.items (id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, vendor_code nchar(120),"
               " barcode nchar(120), name nchar(220), item_url nchar(320), discript text)")
    conn.commit()
    db.execute("CREATE TABLE dbo.photos (id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, vendor_code nchar(120),"
               " barcode nchar(120), photo nchar(220))")
    conn.commit()

# '142.44.136.219:32768', '167.99.54.28:8080', '167.99.126.178:8080', '134.122.113.7:8080','52.143.81.17:3128', '51.222.197.136:32768', '188.240.71.213:3128',
#              '165.227.163.91:3128', '138.68.148.15:8080', '51.158.123.35:9999', '167.99.215.163:8080','176.9.139.181:8080'
#              '150.136.5.47:80', '167.99.126.178:8080', '162.255.201.37:8080', '198.50.163.192:3129',
proxy_lst = ['52.143.81.17:3128',
             '138.68.148.15:8080'
             ]
GLOBAL_URL = 'https://k2.com.pl'


def get_html(url):
    x = True

    while x == True:
        rand_ip = choice(proxy_lst)
        print(rand_ip)
        prox = {"http": "http://" + rand_ip, "https": "http://" + rand_ip}
        try:
            req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
        except:
            print("try")
        else:
            x = False
            if req.status_code == 200:
                return req.content
            else:
                print("ERROR ", url)



def parsing_other_shops(categories):
    # print(categories)
    # file_cardos = open('cardos', "a+")
    # main_URL = "http://masner.com"
    # cardos_html = get_html(url)
    # cardos_soup = BeautifulSoup(cardos_html, "html.parser")
    # category_cardos = cardos_soup.find(class_="catid-120").find("a").get("href")
    #
    # cardos_link = main_URL + category_cardos
    # html_pagination = get_html(cardos_link)
    # if html_pagination != None:
    #     pagination_soup = BeautifulSoup(html_pagination, "html.parser")
    #     max_pagination = pagination_soup.find(class_="pagination").find_all("a")[-1].get("href").split("=")[1]
    #     print(max_pagination)
    #     for i in range(1, int(max_pagination) + 1):
    #         link_with_pagination = cardos_link + "?page=" + str(i)
    #         cardos_items = get_html(link_with_pagination)
    #         items_soup = BeautifulSoup(cardos_items, "html.parser")
    #         all_blocks = items_soup.find_all(class_="block")
    #         for block in all_blocks:
    #             item_url = block.find("a").get("href")
    #             file_cardos.write(main_URL + item_url + '\n')
    #     file_cardos.close()
    # else:
    #     print("error")
    file_card = open('cardos', 'r')
    cardos_lst = file_card.readlines()

    for el in cardos_lst:

        print(el.strip())
        product_html = get_html(el.strip())
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
            db.execute(f"insert into   dbo.items (vendor_code, barcode, name, item_url, discript) VALUES ("
                       f"N'{index}',N'{barcode}', N'{name}', N'{el.strip()}', N'{common_descript}')")
            conn.commit()

            imgs = soup.find(class_="previews").find_all('a')
            for photo_href in imgs:
                photo = photo_href.get("href")
                db.execute(f"insert into  dbo.photos (vendor_code, barcode, photo) VALUES ("
                           f"N'{index}', N'{barcode}',N'{photo}')")
                conn.commit()

        else:
            print("product is out in stock ", el)




def writing_db():
    db.execute("select vendor_code, barcode, name, item_url, discript from dbo.items")
    all_result = db.fetchall()


    sql = "insert into k2.items (vendor_code, barcode, name, item_url, discript) values(%s, %s, %s, %s, %s)"
    db_ms.executemany(sql, all_result)
    conn_ms.commit()

    db.execute("select vendor_code, barcode, photo  from dbo.photos")
    all_result = db.fetchall()


    sql = "insert into k2.photos (vendor_code, barcode, photo) values(%s, %s, %s)"
    db_ms.executemany(sql, all_result)
    conn_ms.commit()

url = 'http://masner.com/produkty/wedlug-serii'


# creating()
# parsing_other_shops(url)
# writing_db()