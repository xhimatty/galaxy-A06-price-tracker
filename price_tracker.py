from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import random
import pandas as pd
from datetime import datetime, date
import time
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

def generate_user_agent():
    chrome_trains = {
        146: 7680,
        147: 7727,
        148: 7778,
    }   

    chrome_major = random.choice(list(chrome_trains.keys()))
    chrome_build = chrome_trains[chrome_major]
    chrome_patch = random.randint(50, 190)

    chrome_version = f"{chrome_major}.0.{chrome_build}.{chrome_patch}"

    os_options = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 11.0; Win64; x64",
        "Macintosh; Intel Mac OS X 13_6_1",
        "Macintosh; Intel Mac OS X 14_2_1",
    ]

    os_string = random.choice(os_options)

    return (
        f"Mozilla/5.0 ({os_string}) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
    )

selected_user_agent = generate_user_agent()

def price_tracker():
    stealth_config = Stealth()
    with stealth_config.use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
        context = None
        try:
            context = browser.new_context(
                user_agent=selected_user_agent,
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                }

            )
            page = context.new_page()
            page.goto('https://www.jumia.com.ng/catalog/?q=samsung+a06+128gb&official_store=1#catalog-listing')
            page.mouse.move(100, 200)
            page.wait_for_timeout(random.randint(1500, 3000))

            page.mouse.wheel(0, random.randint(400, 800))
            page.wait_for_timeout(random.randint(1000, 2500))

            try:
                page.locator('article.prd').first.wait_for(state='visible', timeout=50000)
                articles = page.locator('article.prd')
            except Exception as e:
                log_error(f"Failed to load products: {e}")
                screenshot_path = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                log_error(f"Screenshot saved to {screenshot_path}")
                raise

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

        finally:
            if context:
                context.close()
            browser.close()

    return data

def scrape_with_retry(max_retries=3, wait_seconds=10):
    last_exception = None

    for attempt in range(1, max_retries + 1):
        log_info(f"Scrape attempt {attempt} of {max_retries}")
        try:
            return price_tracker()
        except Exception as e:
            last_exception = e
            log_error(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                wait = wait_seconds * (2 ** (attempt - 1))
                log_info(f"Waiting {wait}s before retry...")
                time.sleep(wait)

    raise RuntimeError(f"All {max_retries} attempts failed. Last error: {last_exception}")


if __name__ == '__main__':
    if date.today() > date(2026, 4, 21):
        log_info("Schedule expired. Program stopped!")
        exit(0)

    log_info("Price tracking started.")
    data = scrape_with_retry(max_retries=3, wait_seconds=10)
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
