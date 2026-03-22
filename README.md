# Galaxy A06 Price Tracker

An automated solution for tracking Samsung Galaxy A06 128GB prices on Jumia. Built with Python and Playwright, it logs product prices, detects changes, and maintains a historical record. Fully automated via GitHub Actions for daily execution, providing reliable insights into price trends with minimal maintenance.

# Tech Stack
    Python · Playwright · Pandas · GitHub Actions

# How It Works
The scraper launches a headless Chromium browser, navigates to the Jumia catalog, extracts product titles, current prices, and original prices, then compares them against the previous day's data before saving everything to price_tracker_data.csv.
GitHub Actions triggers the script every day at 9AM UTC, commits the updated CSV back to the repository, and keeps a full price history over time.
