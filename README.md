# Automated Daily Price Intelligence Tracker – Samsung Galaxy A06 (Jumia Nigeria)

A fully automated price monitoring solution that tracks listings for the Galaxy A06 on Jumia.com.ng. The solution runs daily at 09:00 UTC via GitHub Actions, extracts real-time pricing data using Playwright, and maintains a clean historical dataset with intelligent change detection.

Using pandas for data processing and incremental CSV updates, the tracker automatically classifies each price movement (new, increased, decreased, no change) while preserving complete historical records. It includes robust error handling, structured logging, anti-bot resilience techniques, and a built-in expiration safeguard.

This solution is configured to run for a fixed duration of 4 weeks and 3 days, after which execution stops automatically. It delivers continuous competitive intelligence on pricing dynamics, ensures reliable data collection, and provides a scalable foundation for advanced analytics such as dashboards or predictive modeling.

## Key Features

#### Core Functionality
- Reliable browser automation using Playwright (Chromium) for dynamic JavaScript-rendered pages  

- Daily change detection and flagging against last-known historical prices

- Local CSV "data lake" with detailed logging system to track execution health, errors, and lifecycle milestones.

- Idempotent design to allow safe repeated execution without data duplication

#### Automation and Pipeline
- Integrated with GitHub Actions to execute on a daily cron schedule, ensuring consistent data collection with automated commits without manual intervention.

- Built-in expiration logic for controlled execution timeline (4 weeks + 3 days) to prevent indefinite runs.

#### Anti-Bot & Stealth Enhancements
- Integration of playwright-stealth to reduce detection by anti-bot systems

- Auto-generated rotating user agents to simulate real browser traffic and reduce fingerprinting

- Custom browser launch arguments to mask automation signals

- Simulated human-like interactions including mouse movement and scrolling behavior

#### Resilience and Reliability
- Enhanced retry logic using exponential backoff

- Improved delay handling for better recovery from transient failures and rate limits

- Graceful error handling to prevent full pipeline failure on partial errors

## Tech Stack
    Python · Playwright · Pandas · GitHub Actions

## Key Outcomes
- **Historical Accuracy:** Captures the "Old Price" vs. "Current Price" to identify artificial vs. genuine discounts.

- **Efficiency:** Automated CI/CD workflow eliminates the need for dedicated server infrastructure, running entirely on GitHub’s ephemeral runners.

- **Actionable Insights:** Provides a clean, time-stamped audit trail ready for visualization in BI tools like Power BI or Tableau.
## How It Works
The scraper launches a headless Chromium browser with stealth configurations, randomized user agents, and anti-detection measures. It navigates to the Jumia catalog, extracts product titles, current prices, and original prices, then compares them against the previous day's data before saving everything to price_tracker_data.csv.

Human-like interactions such as mouse movement and scrolling are simulated to improve scraping reliability.

GitHub Actions triggers the script every day at 9AM UTC, commits the updated CSV back to the repository, and keeps a full price history over time.
