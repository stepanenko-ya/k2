import pymssql
import time

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")

db = conn.cursor()
db.execute("select  vendor_code, barcode, name, item_url, discript from k3.items")
result = db.fetchall()

sql = "insert into k2.items (vendor_code, barcode, name, item_url, discript) values(%s, %s, %s, %s, %s)"
db.executemany(sql, result)
conn.commit()


# db.execute("DELETE  FROM k2.items WHERE item_url LIKE'%cardos%'")
# conn.commit()
