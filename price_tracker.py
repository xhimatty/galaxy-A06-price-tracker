from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime, date
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    filename='price_tracker.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)

def price_tracker():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.jumia.com.ng/catalog/?q=samsung+a06+128gb&official_store=1#catalog-listing')
        page.locator('article.prd').first.wait_for(state='visible')
        articles = page.locator('article.prd')

        data = []
        count = articles.count()
        for i in range(count):
            try:
                title = articles.nth(i).locator('h3.name').inner_text().strip()
            except Exception as e:
                log_error(f"Error fetching title for article {i}: {e}")
                title = "N/A"
            try:
                price = articles.nth(i).locator('div.prc').inner_text().strip()
            except Exception as e:
                log_error(f"Error fetching price for article {i}: {e}")
                price = "N/A"
            try:
                old_price = articles.nth(i).locator('div.old').inner_text().strip()
            except Exception as e:
                log_error(f"Error fetching old price for article {i}: {e}")
                old_price = "N/A"
            date_scraped = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            data.append({
                'title': title,
                'price': price,
                'old_price': old_price,
                'date': date_scraped
            })

        browser.close()

    return data

if __name__ == '__main__':
    if date.today() > date(2026, 4, 21):
        log_info("Schedule expired. Program stopped!")
        exit(0)

    log_info("Price tracking started.")
    data = price_tracker()
    log_info('Price tracking completed')

    df = pd.DataFrame(data)
    csv_file = 'price_tracker_data.csv'

    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)

        last_prices = existing_df.groupby('title')['price'].last().to_dict()

        def clean_price(p):
            try:
                return int(str(p).replace('₦', '').replace(',', ''))
            except:
                return None
            
        changes = []
        for x, row in df.iterrows():
            title = row['title']
            current_price = clean_price(row['price'])
            previous_price_raw = last_prices.get(title)
            previous_price = clean_price(previous_price_raw) if previous_price_raw else None

            if previous_price is None:
                change = "new"
            elif current_price is None:
                change = "unknown"
            elif current_price > previous_price:
                change = "increased"
            elif current_price < previous_price:
                change = "decreased"
            else:
                change = "no change"

            changes.append(change)

        df['change'] = changes

        dfs = pd.concat([existing_df, df], ignore_index=True)
    else:
        df['change'] = 'new'
        dfs = df

    dfs.to_csv(csv_file, index=False)
    log_info(f"Saved data to {csv_file}. Total records: {len(dfs)}")
