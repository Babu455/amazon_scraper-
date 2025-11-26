import time
import random
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class AmazonSeleniumScraper:
    def __init__(self, headless=False):

        chrome_options = Options()

        
        if headless:
            chrome_options.add_argument('--headless')

        
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Chrome(options=chrome_options)

            # Fix webdriver detection
            self.driver.execute_cdp_cmd(
                'Page.addScriptToEvaluateOnNewDocument',
                {
                    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                }
            )

        except Exception as e:
            print(f"Error initializing ChromeDriver: {e}")
            raise

        self.products = []
        self.wait = WebDriverWait(self.driver, 15)

    def get_search_url(self, page=1):
        return f"https://www.amazon.in/s?k=laptop&page={page}"

    def scroll_page(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(3):
            self.driver.execute_script(f"window.scrollTo(0, {(i + 1) * (last_height // 3)});")
            time.sleep(random.uniform(0.6, 1.2))

    def get_total_pages(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.s-pagination-item")))
            elements = self.driver.find_elements(By.CSS_SELECTOR, "span.s-pagination-item")
            nums = []

            for el in elements:
                t = el.text.strip()
                if t.isdigit():
                    nums.append(int(t))

            if nums:
                total = max(nums)
                print(f"\nTotal pages detected: {total}")
                return total

            return 1

        except:
            return 1

    def extract_products_from_page(self):
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
            ))

            self.scroll_page()

            product_cards = self.driver.find_elements(By.CSS_SELECTOR,
                                                      '[data-component-type="s-search-result"]')

            print(f"Found {len(product_cards)} products")

            for card in product_cards:
                try:
                    data = {
                        "Image": self.extract_image(card),
                        "Title": self.extract_title(card),
                        "Rating": self.extract_rating(card),
                        "Price": self.extract_price(card),
                        "Result_Type": self.check_sponsored(card)
                    }

                    if data["Title"] != "No Title":
                        self.products.append(data)

                except:
                    continue

            return True

        except TimeoutException:
            print("Timeout loading product list")
            return False

    def extract_image(self, product):
        try:
            return product.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
        except:
            return "No Image"

    def extract_title(self, product):
        try:
            return product.find_element(By.CSS_SELECTOR, "h2 span").text.strip()
        except:
            return "No Title"

    def extract_rating(self, product):
        try:
            rating_text = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt") \
                                 .get_attribute("textContent")
            return rating_text.split()[0] if rating_text else "No Rating"
        except:
            return "No Rating"

    def extract_price(self, product):
        try:
            return "₹" + product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
        except:
            try:
                return product.find_element(By.CSS_SELECTOR, "span.a-offscreen") \
                    .get_attribute("textContent")
            except:
                return "No Price"

    def check_sponsored(self, product):
        try:
            product.find_element(By.XPATH, ".//*[contains(text(),'Sponsored')]")
            return "Ad"
        except:
            return "Organic"

    def scrape_multiple_pages(self, total_pages):
        for page in range(1, total_pages + 1):
            url = self.get_search_url(page)
            print(f"\nScraping Page {page}/{total_pages}: {url}")

            self.driver.get(url)
            time.sleep(random.uniform(2, 4))

            if not self.extract_products_from_page():
                break

            print(f"Total collected: {len(self.products)} items")
            time.sleep(random.uniform(2, 4))

    def save_to_csv(self):
        if not self.products:
            print("No data found!")
            return

        df = pd.DataFrame(self.products)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amazon_laptops_{timestamp}.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print("\n============================================")
        print(f"Saved File: {filename}")
        print(f"Total Products: {len(df)}")
        print("============================================")

    def close(self):
        self.driver.quit()


def main():
        print("=" * 50)
        print("   AMAZON LAPTOP SCRAPER (SELENIUM)")
        print("=" * 50)

        scraper = AmazonSeleniumScraper(headless=False)

        scraper.driver.get(scraper.get_search_url(1))
        time.sleep(3)

        total_pages = scraper.get_total_pages()

        scraper.scrape_multiple_pages(total_pages)
        scraper.save_to_csv()
        scraper.close()


if __name__ == "__main__":
    main()
