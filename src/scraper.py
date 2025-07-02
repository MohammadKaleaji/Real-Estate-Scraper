# src/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time

class AqarScraper:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://sa.aqar.fm"

    def scrape(self, city="الرياض", max_price=500000, pages=1):
        results = []
        for page in range(1, pages+1):
            url = f"{self.base_url}/شقق-للبيع/{city}?page={page}"
            self.driver.get(url)
            
            # Wait for listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".listing-card"))
            )
            
            listings = self.driver.find_elements(By.CSS_SELECTOR, ".listing-card")
            for listing in listings:
                try:
                    price_text = listing.find_element(By.CSS_SELECTOR, ".listing-price").text
                    price = int(price_text.replace("ر.س", "").replace(",", "").strip())
                    
                    if price <= max_price:
                        results.append({
                            "title": listing.find_element(By.CSS_SELECTOR, ".listing-title").text,
                            "price": price,
                            "location": listing.find_element(By.CSS_SELECTOR, ".listing-location").text,
                            "link": listing.find_element(By.CSS_SELECTOR, "a.listing-link").get_attribute("href"),
                            "bedrooms": self._safe_extract(listing, ".listing-rooms span"),
                            "size": self._safe_extract(listing, ".listing-area span")
                        })
                except NoSuchElementException:
                    continue
            
            time.sleep(2)  # Be polite
        
        self.driver.quit()
        return results

    def _safe_extract(self, element, selector):
        try:
            return element.find_element(By.CSS_SELECTOR, selector).text
        except:
            return "N/A"

    def save_to_csv(self, data, filename="src/output/results.csv"):
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)