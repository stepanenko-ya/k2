import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymssql
import time

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

db = conn.cursor()

GLOBAL_URL = 'https://k2.com.pl'


proxy_lst = ['186.167.20.211:3128', '190.14.249.139:999', '167.99.126.178:8080', '46.101.83.76:8080',
             '191.96.60.182:31210', '188.166.245.147:8080', '210.113.204.108:8080', '159.65.43.120:8080',
             '203.74.120.79:3128', '194.5.206.148:3128', '167.99.54.28:8080', '144.91.95.126:3128',
             '183.88.226.50:8080', '132.248.196.2:8080', '202.61.51.204:3128', '217.218.66.76:80', '100.26.11.72:80',
             '51.158.123.35:9999'
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
            if req.status_code != 200:
                x = True
                req = requests.get(url, headers={"User-Agent": UserAgent().chrome}, proxies=prox, timeout=10)
            return req.text


def category():
    categories_lst = []
    content_html = get_html(main_url, proxy_lst)
    soup = BeautifulSoup(content_html, "html.parser")
    finders = soup.find(class_="category-list")
    for item in finders.select("ul.child-category-list"):
        item.decompose()
    s = finders.find_all("li")
    for li in s:
        link = li.find("a").get("href")
        if link[0] == '/':
            categories_lst.append(GLOBAL_URL + link)
        else:
            categories_lst.append(link + '\n')
    return categories_lst

    # url = "https://k2.com.pl/produkty"
    # html = get_html(url, proxy_lst)
    #
    # soup = BeautifulSoup(html, "html.parser")
    # finders = soup.find_previous(class_="fa fa-arrow-down")
    # print(finders)
    # # for finder in finders:
    # #     url = finder.find("a").get("href")
    # #     print(url)
    # # for finder in finders:
    # #     url = finder.find("a").get('href')
    # #
    # #     urls_file = open('categories.txt', "a+")
    # #     urls_file.write(GLOBAL_URL + url + '\n')
    # #     urls_file.close()


def parsing_items_url(categories):
    file_items_urls = open("items_url.txt", "a+")
    for cat_url in categories[:-2]:
        html_product = get_html(cat_url.strip(), proxy_lst)
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


def parsing_other_shops(categories):

    for cat_url in categories:
        if cat_url.strip() == 'http://cardos.com/produkty':
            # file_cardos = open('cardos', "a+")
            # cardos_URL = "http://cardos.com"
            # cardos_html = get_html(cat_url.strip(), proxy_lst)
            # cardos_soup = BeautifulSoup(cardos_html, "html.parser")
            # category_cardos = cardos_soup.find(class_="catid-120").find("a").get("href")
            # cardos_link = cardos_URL + category_cardos
            #
            # html_pagination = get_html(cardos_link, proxy_lst)
            # pagination_soup = BeautifulSoup(html_pagination, "html.parser")
            # max_pagination = pagination_soup.find(class_="pagination").find_all("a")[-1].get("href").split("=")[1]
            #
            # for i in range(1, int(max_pagination) + 1):
            #     link_with_pagination = cardos_link + "?page=" + str(i)
            #     cardos_items = get_html(link_with_pagination, proxy_lst)
            #     items_soup = BeautifulSoup(cardos_items, "html.parser")
            #     all_blocks = items_soup.find_all(class_="block")
            #     for block in all_blocks:
            #         item_url = block.find("a").get("href")
            #         file_cardos.write(cardos_URL + item_url + '\n')
            # file_cardos.close()
            file_card = open('cardos', 'r')
            cardos_lst = file_card.readlines()

            for el in cardos_lst:
                time.sleep(13)
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
                    db.execute(f"INSERT INTO {schema_name}.photos ("
                               f"vendor_code, barcode, photo) VALUES (N'{index}', N'{barcode}', N'{photo}')")
                    conn.commit()

        elif cat_url.strip() == 'http://masner.com/produkty':
            pass


def parsing_product():

    items_list = open("items_url.txt", "r")
    items_set = set(items_list.readlines())

    for item in list(items_set):
        if item.strip() != "https://k2.com.pl/produkty/w222-niska-sila-50-g":
            html_content = get_html(item.strip(), proxy_lst)
            soup = BeautifulSoup(html_content, "html.parser")
            # item_file = open('item_file.txt', "a+")
            name = soup.find(class_="col-md-8 product-images").find("h1").get_text().strip()
            description = soup.find(id="opis").get_text()
            shot_descript = soup.find(class_="description-short").get_text()
            desct = shot_descript + description
            all_discript = desct.replace("\n", ' ').replace("'", '')
            numbers = soup.find(class_="product-index").get_text().strip().split("\n")
            index = numbers[0].split(":")[1].strip()
            barcode = numbers[1].split(":")[1].strip()
            # item_file.write(index + "|" + barcode + "|" + name + "|" + item.strip() + "|" + all_discript +"\n")
            # item_file.close()
            db.execute(f"INSERT INTO {schema_name}.items (vendor_code, name, item_url, barcode, discript) VALUES (N'{index}', N'{name}', N'{item.strip()}', N'{barcode}', N'{all_discript}')")
            conn.commit()

            images = soup.find(class_="product-image").find_all("a")
            # photo_file = open('photos.csv', "a+")
            for img in images:
                photo = img.get("href")

            #     photo_file.write(index + "|" + barcode + "|" + photo + "\n")
            # photo_file.close()
                db.execute(f"INSERT INTO {schema_name}.photos ("
                           f"vendor_code,photo) VALUES (N'{index}', N'{photo}')")
                conn.commit()
        else:
            pass


def creating():
    db.execute(f"CREATE SCHEMA {schema_name}")
    conn.commit()

    db.execute(f"CREATE TABLE {schema_name}.items (id int IDENTITY(1,1), "
               f"vendor_code NVARCHAR(230), "
               f"barcode NVARCHAR(330), "
               f"name NVARCHAR(355), "
               f"item_url NVARCHAR(330),"
               f"discript ntext)")
    conn.commit()

    db.execute(f"CREATE TABLE {schema_name}.photos (id int IDENTITY(1,1),  vendor_code NVARCHAR (130), "
               f"barcode NVARCHAR (130), photo NVARCHAR (330))")
    conn.commit()


if __name__ == '__main__':
    main_url = "https://k2.com.pl/produkty"
    schema_name = "k3"
    # creating()
    # categories = category()
    categories_file = open("cat.txt", "r")
    c = categories_file.readlines()
    # parsing_items_url(c)
    # parsing_product()
    parsing_other_shops(c)







