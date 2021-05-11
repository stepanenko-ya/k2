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



db.execute("select  * from k2.items WHERE vendor_code ='P90610'")
result = db.fetchall()
print(result)
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
