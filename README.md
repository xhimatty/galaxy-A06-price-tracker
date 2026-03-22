# Automated Daily Price Intelligence Tracker – Samsung Galaxy A06 (Jumia Nigeria)

A fully automated price monitoring solution that tracks listings for the Galaxy A06 on Jumia.com.ng. The solution runs daily at 09:00 UTC via GitHub Actions, extracts real-time pricing data using Playwright, and maintains a clean historical dataset with intelligent change detection.

Using pandas for data processing and incremental CSV updates, the tracker automatically classifies each price movement (new, increased, decreased, no change) while preserving complete historical records. It includes robust error handling, structured logging, and a built-in expiration safeguard.

This solution delivers continuous competitive intelligence on pricing dynamics, ensures reliable data collection, and provides a scalable foundation for advanced analytics such as dashboards or predictive modeling.

## Key Features
- Reliable browser automation using Playwright (Chromium) for dynamic JavaScript-rendered pages  

- Extraction of title, current price, and old price

- Daily change detection and flagging against last-known historical prices

- Append-only CSV storage for long-term trend analysis

- Integrated with GitHub Actions to execute on a daily cron schedule, ensuring consistent data collection with automated commits without manual intervention.

- Built-in expiration logic for controlled execution timeline to prevent indefinite runs.

- Local CSV "data lake" with detailed logging system to track execution health, errors, and lifecycle milestones.

- Graceful error handling to prevent full pipeline failure on partial errors

- Idempotent design to allow safe repeated execution without data duplication

## Tech Stack
    Python · Playwright · Pandas · GitHub Actions

## Key Outcomes
- **Historical Accuracy:** Captures the "Old Price" vs. "Current Price" to identify artificial vs. genuine discounts.

- **Efficiency:** Automated CI/CD workflow eliminates the need for dedicated server infrastructure, running entirely on GitHub’s ephemeral runners.

- **Actionable Insights:** Provides a clean, time-stamped audit trail ready for visualization in BI tools like Power BI or Tableau.
## How It Works
The scraper launches a headless Chromium browser, navigates to the Jumia catalog, extracts product titles, current prices, and original prices, then compares them against the previous day's data before saving everything to price_tracker_data.csv.
GitHub Actions triggers the script every day at 9AM UTC, commits the updated CSV back to the repository, and keeps a full price history over time.
