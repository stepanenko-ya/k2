import pymssql
import psycopg2


# conn_ms = pymssql.connect(
#     server="10.175.1.60:1433",
#     user="importer_doc",
#     password='QAZxsw123',
#     database="Test")
# db_ms = conn_ms.cursor()

conn_pg = psycopg2.connect(
    host='localhost',
    user='step',
    password='Stomatolog',
    database='yana_db')

db_pg = conn_pg.cursor()
schema_name = "k2"

# def creating():
#     db_ms.execute(f"CREATE SCHEMA {schema_name}")
#     conn_ms.commit()
#
#     db_ms.execute(f"CREATE TABLE {schema_name}.items (id int IDENTITY(1,1), "
#                f"vendor_code NVARCHAR(230), "
#                f"barcode NVARCHAR(330), "
#                f"name NVARCHAR(355), "
#                f"item_url NVARCHAR(330),"
#                f"discript ntext)")
#     conn_ms.commit()
#
#     db_ms.execute(f"CREATE TABLE {schema_name}.photos (id int IDENTITY(1,1),  vendor_code NVARCHAR (130), "
#                f"barcode NVARCHAR (130), photo NVARCHAR (330))")
#     conn_ms.commit()






def writing():

    db_pg.execute("select  vendor_code, barcode, name, item_url, discript from k2.items")
    items_result = db_pg.fetchall()
    print(items_result)
    # sql = "insert into k2.items (vendor_code, barcode, name, item_url, discript) values(%s, %s, %s, %s, %s)"
    # db_ms.executemany(sql, items_result)
    # conn_ms.commit()

    db_pg.execute("select  vendor_code, barcode, photo from k2.photos")
    photo_result = db_pg.fetchall()
    print(photo_result)

    # sql = "insert into k2.photos (vendor_code, barcode, photo) values(%s, %s, %s)"
    # db_ms.executemany(sql, photo_result)
    # conn_ms.commit()


# creating()
writing()



