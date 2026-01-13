import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EcomAutomationExpert:
    """
    核心业务逻辑类：将抓取与数据处理解耦
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        self.raw_data = []

    def fetch_product_page(self, url):
        """抓取原始数据 - 包含异常处理逻辑"""
        try:
            logging.info(f"正在请求页面: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status() 
            return response.content
        except Exception as e:
            logging.error(f"网络请求失败: {e}")
            return None

    def parse_html(self, html_content):
        """解析 HTML - 模拟多选择器兼容逻辑"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = soup.find(id='productTitle').get_text().strip() if soup.find(id='productTitle') else "Unknown"
        price_raw = soup.find(class_='a-price-whole').get_text().strip() if soup.find(class_='a-price-whole') else "0"
        
        item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": title,
            "price_raw": price_raw,
            "source_url": "Amazon" 
        }
        self.raw_data.append(item)
        return item

    def process_with_pandas(self):
        """
        核心卖点：使用 Pandas 进行数据清洗与分析
        """
        if not self.raw_data:
            return "No data to process."

        df = pd.DataFrame(self.raw_data)
       
        df['price_clean'] = df['price_raw'].str.replace(',', '').astype(float)
        
        summary = {
            "average_price": df['price_clean'].mean(),
            "item_count": len(df)
        }
        
        filename = f"report_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"报告已生成并清洗完毕: {filename}")
        return summary

if __name__ == "__main__":
    
    urls = ["https://www.amazon.com/dp/B08N5KWB9H"] 
    
    expert = EcomAutomationExpert()
    
    for url in urls:
        content = expert.fetch_product_page(url)
        if content:
            expert.parse_html(content)
            time.sleep(2) 

    result = expert.process_with_pandas()
    print(f"--- 任务完成 ---\n数据摘要: {result}")
