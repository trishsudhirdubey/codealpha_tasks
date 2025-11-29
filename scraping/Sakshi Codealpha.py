import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN, en;q=0.9"
}

def parse_search_page(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("Request failed:", r.status_code, " — ", url)
        return []
    soup = BeautifulSoup(r.content, "lxml")
    items = soup.find_all("div", {"data-component-type": "s-search-result"})
    results = []
    for item in items:
        title = item.h2.text.strip() if item.h2 else ""
        price_whole = item.find("span", class_="a-price-whole")
        price_frac = item.find("span", class_="a-price-fraction")
        price = ""
        if price_whole:
            price = price_whole.text.strip()
            if price_frac:
                price += price_frac.text.strip()
        rating_span = item.find("span", class_="a-icon-alt")
        rating = rating_span.text.strip() if rating_span else ""
        # optional: more detail, e.g. specs block
        specs = ""
        spec_div = item.find("div", class_="a-row a-size-base a-color-secondary")
        if spec_div:
            specs = spec_div.text.strip().replace("\n", " | ")
        results.append({
            "Product Name": title,
            "Price (INR)": price,
            "Rating": rating,
            "Specs / Description": specs
        })
    return results

def scrape_amazon(max_pages=5, delay=(2, 5)):
    all_data = []
    base_url = "https://www.amazon.in/s?k=phone+under+30k"
    for page in range(1, max_pages+1):
        url = f"{base_url}&page={page}"
        print("Scraping:", url)
        page_data = parse_search_page(url)
        all_data.extend(page_data)
        time.sleep(random.uniform(*delay))
    df = pd.DataFrame(all_data)
    df.to_csv("amazon_mobiles_under_30k.csv", index=False)
    print("Saved", len(df), "records to amazon_mobiles_under_30k.csv")

if __name__ == "__main__":
    scrape_amazon(max_pages=15)
