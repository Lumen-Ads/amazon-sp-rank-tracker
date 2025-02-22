import logging
import pandas as pd
import time
import random
import threading
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from src.utils.excel_handler import save_to_excel

class AmazonScraper:
    def __init__(self):
        self.driver = None
        self.processing = False

    def setup_selenium(self):
        ua = UserAgent()
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--log-level=3")
        firefox_options.add_argument(f"user-agent={ua.random}")
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)

    def upload_file(self, file_path):
        try:
            df = pd.read_excel(file_path)
            if 'ASINs' not in df.columns or 'Keywords' not in df.columns:
                raise ValueError("Excel file must contain 'ASINs' and 'Keywords' columns")
            
            self.uploaded_data = {
                'asins': df['ASINs'].tolist(),
                'keywords': df['Keywords'].tolist()
            }
        except Exception as e:
            logging.error(f"Error reading Excel file: {e}")
            raise

    def find_sponsored_product_rank(self, keyword, asin, max_retries=5):
        url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
        
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                self.wait_for_page_load(self.driver)
                
                if self.check_for_captcha(self.driver):
                    return "CAPTCHA"
                
                if not self.wait_for_sponsored_products(self.driver):
                    if attempt == max_retries - 1:
                        return "Timeout - No Sponsored Products"
                    continue
                
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                sponsored_products = self.find_sponsored_products(soup)
                
                if not sponsored_products:
                    if attempt == max_retries - 1:
                        return "Not Found"
                    continue
                
                sponsored_position = 1
                for product in sponsored_products:
                    product_asin = product.get("data-asin")
                    if product_asin == asin:
                        return sponsored_position
                    sponsored_position += 1
                
                return "Not Found"
                
            except Exception as e:
                logging.error(f"Error finding sponsored product rank: {e}")
                if attempt == max_retries - 1:
                    return "Error"
                time.sleep(random.uniform(1, 4))
        
        return "Not Found"

    def process_data(self, data, progress_callback):
        self.setup_selenium()
        self.processing = True
        placements = []
        total = len(data['asins'])
        
        try:
            for i, (asin, keyword) in enumerate(zip(data['asins'], data['keywords'])):
                if not self.processing:
                    break
                    
                placement = self.find_sponsored_product_rank(keyword, asin)
                placements.append({
                    'Keyword': keyword,
                    'ASIN': asin,
                    'Sponsored Placement': placement
                })
                
                progress_callback(i + 1, total)
                time.sleep(random.uniform(3, 6))
                
        except Exception as e:
            logging.error(f"Error in process_data: {e}")
        finally:
            if self.driver:
                self.driver.quit()
            self.processing = False
            
        return placements

    def wait_for_page_load(self, driver, timeout=40):
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            logging.warning("Page load timeout - proceeding anyway")

    def check_for_captcha(self, driver):
        try:
            driver.find_element(By.ID, "captchacharacters")
            return True
        except NoSuchElementException:
            return False

    def wait_for_sponsored_products(self, driver, timeout=40):
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='sp-sponsored-result'], .s-result-item.AdHolder"))
            )
            return True
        except TimeoutException:
            return False

    def find_sponsored_products(self, soup):
        sponsored_products = []
        sp_sponsored = soup.find_all('div', attrs={"data-component-type": "sp-sponsored-result"})
        sponsored_products.extend(sp_sponsored)
        
        ad_holders = soup.find_all('div', class_="s-result-item AdHolder")
        sponsored_products.extend(ad_holders)
        
        search_results = soup.find_all('div', attrs={"data-component-type": "s-search-result"})
        for result in search_results:
            sponsored_label = result.find('span', string=lambda text: text and 'Sponsored' in text)
            if sponsored_label:
                sponsored_products.append(result)
        
        return sponsored_products