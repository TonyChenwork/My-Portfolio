import requests
from bs4 import BeautifulSoup
import time
import csv

# 这是模拟一个电商网站价格监控的自动化脚本
# Target: E-commerce product page
# Function: Scrape price and title, save to CSV

def get_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 模拟抓取标题和价格 (Mock selectors)
            title = soup.find(id='productTitle').get_text().strip()
            price = soup.find(class_='a-price-whole').get_text().strip()
            
            print(f"Success! Found product: {title}")
            print(f"Current Price: {price}")
            return title, price
        else:
            print("Failed to retrieve the page.")
            return None, None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    # 示例 URL
    target_url = "https://www.amazon.com/dp/B08N5KWB9H"
    
    print("Starting Price Tracker...")
    get_product_info(target_url)
    print("Task Completed.")
