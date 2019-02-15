import argparse
import requests
import json
import pymongo
# 下载知乎书籍的数据
def get_books_by_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
    r = requests.get(url, headers=headers)
    data = json.loads(r.content.decode("utf-8"))
    return data

def get_books_by_category(category_id):
    url_patt = "https://www.zhihu.com/api/v3/books/categories/{}?limit={}&offset={}&version=v2"
    limit = 10
    offset = 0
    client = pymongo.MongoClient('10.18.6.26',27001)
    db = client.zhihu_book
    while True:
        url = url_patt.format(category_id, limit, offset)
        print(url)
        data = get_books_by_url(url)
        books = data["data"]
        db.books.insert_many(books)
        if data["paging"]["is_end"]:
            break
        offset = offset + limit

def get_all_books():
    categories = [147, 254, 232, 209, 245, 175, 219, 189, 205, 161, 143, 284, 265, 214, 155, 241]
    for category in categories:
        get_books_by_category(category)

def query_books():
    client = pymongo.MongoClient('10.18.6.26',27001)
    db = client.zhihu_book

    books = db.books.find().sort("score")
    book_ids = []
    for book in books:
        if book["id"] in book_ids:
            continue
        price = 0
        if book["promotion"]["is_promotion"]:
            price = book["promotion"]["promotion_price"]/100
        else:
            price = book["promotion"]["price"]/100
        print("{},{},{},{},{}".format(book["title"], book["url"], book["score"], price, book["promotion"]["origin_price"]/100))
        book_ids.append(book["id"])

#    books = db.books.find({"promotion.price": 0.0}).sort("score")
#    book_ids = []
#    for book in books:
#        if book["id"] in book_ids:
#            continue
#        print("{},{},{}".format(book["title"], book["url"], book["score"]))
#        book_ids.append(book["id"])

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--download", help="", action="store_true")
    # parser.add_argument("--query", help="", action="store_true")
    # args = parser.parse_args()
    # if args.download:
    #     get_all_books()
    # elif args.query:
    #     query_books()
    get_all_books()