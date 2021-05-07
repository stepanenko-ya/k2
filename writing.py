import random
import requests
from random import choice
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymssql

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

db = conn.cursor()


def write_photos():
    with open("photos.csv") as file_photo:
        file_photo = file_photo.readlines()
        for photo in file_photo:
            result_photo = photo.strip().split("|")
            db.execute(f"INSERT INTO {schema_name}.photos ("
                       f"vendor_code, barcode, photo) VALUES ("
                       f"N'{result_photo[0]}', N'{result_photo[1]}', N'{result_photo[2]}')")
            conn.commit()


def write_items():
    with open("item_file.txt") as file_items:
        items = file_items.readlines()
        for item in items:
            result_item = item.strip().split("|")
            print(result_item[2])

            db.execute(f"INSERT INTO {schema_name}.items ("
                       f"vendor_code, barcode, name, item_url,  discript) VALUES ("
                       f"N'{result_item[0]}', N'{result_item[1]}', N'{result_item[2]}', N'{result_item[3]}', N'{result_item[4]}')")
            conn.commit()




if __name__=="__main__":
    schema_name = 'k2'
    # write_photos()
    write_items()
