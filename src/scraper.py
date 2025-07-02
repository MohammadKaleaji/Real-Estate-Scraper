# src/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class AqarScraper:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.base_url = "https://sa.aqar.fm"

    def _click_search_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._search__NZ4FA"))
        ).click()
        time.sleep(1)

    def _select_city(self, city_name="الرياض"):
        city_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select-module_label__VrX38"))
        )
        city_dropdown.click()
        time.sleep(0.5)
        
        city_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'select-module_option__3YibH') and text()='{city_name}']"))
        )
        city_option.click()
        time.sleep(0.5)

    def _set_max_price(self, max_price):
        price_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='السعر الأعلى']"))
        )
        price_input.clear()
        price_input.send_keys(str(max_price))
        time.sleep(0.3)

    def _execute_search(self):
        search_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-module_primary__z30up"))
        )
        search_btn.click()
        time.sleep(2)

    def scrape(self, city="الرياض", max_price=500000, pages=1):
        self.driver.get(self.base_url)
        time.sleep(2)
        
        self._click_search_button()
        self._select_city(city)
        self._set_max_price(max_price)
        self._execute_search()
        
        all_data = []
        for _ in range(pages):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".listing-card"))
            )
            
            listings = self.driver.find_elements(By.CSS_SELECTOR, ".listing-card")
            for listing in listings:
                try:
                    all_data.append({
                        "Title": listing.find_element(By.CSS_SELECTOR, ".listing-title").text,
                        "Price": listing.find_element(By.CSS_SELECTOR, ".listing-price").text,
                        "Location": listing.find_element(By.CSS_SELECTOR, ".listing-location").text,
                        "Bedrooms": listing.find_element(By.CSS_SELECTOR, ".listing-rooms span").text,
                        "Size": listing.find_element(By.CSS_SELECTOR, ".listing-area span").text,
                        "Link": listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    })
                except:
                    continue
            
            break  # Remove for pagination
        
        self.driver.quit()
        return pd.DataFrame(all_data)