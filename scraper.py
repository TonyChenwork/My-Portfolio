import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_books():
    print("--- Book Scraper Pro v1.0 by Wayen ---")
    print("Target: books.toscrape.com")

    # 目标网址（专门供练习的爬虫靶场）
    url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

    response = requests.get(url)

    # 如果连接成功 (状态码 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        data = []

        for book in books:
            # 1. 抓取书名
            title = book.h3.a["title"]

            # 2. 抓取价格
            price = book.find("p", class_="price_color").text

            # 3. 抓取状态
            availability = book.find("p", class_="instock availability").text.strip()

            # 4. 抓取评分 (例如 "Three")
            rating = book.p["class"][1]

            print(f"Got: {title[:20]}... | {price}")

            data.append({
                "Book Title": title,
                "Price": price,
                "Stock Status": availability,
                "Rating": f"{rating} Stars"
            })

        # 保存为 Excel
        df = pd.DataFrame(data)
        df.to_excel("book_data_sample.xlsx", index=False)
        print("\nSuccess! Data saved to 'book_data_sample.xlsx'")

    else:
        print("Failed to connect.")


if __name__ == '__main__':
    scrape_books()