# SaaS Product Review Scraper
**Pulse Coding Assignment**

## Overview
This project is a Python-based SaaS product review scraper developed for the Pulse Coding Assignment.  
It collects and aggregates product reviews from multiple platforms based on a given company name and date range.

The solution focuses on clean architecture, modular design, and robust error handling.

---

## Objectives
- Scrape SaaS product reviews from **G2** and **Capterra**
- Filter reviews based on a specified time period
- Export results in **JSON format**
- **Bonus**: Integrate a third SaaS review platform (**TrustRadius**)

---

## Features
- Command-line interface (CLI) based execution
- Multi-source review aggregation
- Date range filtering
- Structured JSON output with metadata
- Graceful handling of blocked or inaccessible pages
- Modular and extensible code design
- Demo mode for safe execution without live scraping

---

## Supported Platforms
- G2
- Capterra
- TrustRadius (Bonus)

---

## Project Structure
review_scraper/
├── scraper/
│ ├── base_scraper.py
│ ├── g2_scraper.py
│ ├── capterra_scraper.py
│ ├── trustradius_scraper.py
│ └── utils.py
├── main.py
├── requirements.txt
├── README.md
├── reviews_output.json

---

## Installation
Ensure Python 3.9 or above is installed.

```bash
pip install -r requirements.txt
Usage
Demo Mode (Recommended)

Demo mode generates realistic mock reviews and avoids platform access restrictions.
python main.py --company "Slack" --demo
Live Scraping Mode
python main.py --company "Slack" --start-date 2024-01-01 --end-date 2024-12-31 --source all --verbose
Note:
Live scraping may return 403 Forbidden responses due to platform bot protection.
This behavior is expected and handled gracefully without crashing the application.
Input Parameters
| Argument       | Description                       |
| -------------- | --------------------------------- |
| `--company`    | SaaS product or company name      |
| `--start-date` | Start date (YYYY-MM-DD)           |
| `--end-date`   | End date (YYYY-MM-DD)             |
| `--source`     | g2 / capterra / trustradius / all |
| `--output`     | Output JSON file (optional)       |
| `--verbose`    | Enable detailed logging           |
| `--demo`       | Run in demo mode                  |
**Output**

The script generates a JSON file containing:

Metadata (company name, date range, source, execution time)

Review details (title, text, date, rating, source)

**Error Handling**

Network and request failures are safely handled

Blocked requests are logged as warnings

Missing or malformed data is skipped

Empty results still produce valid JSON outpu

**Ethical Considerations**

No aggressive scraping techniques used

No bypassing of platform security mechanisms

Designed strictly for educational purposes

Demo mode included to ensure compliance with platform policies

**Bonus Implementation**

A third SaaS review platform, TrustRadius, has been integrated using the same architecture as the primary sources, fulfilling the bonus requirement.

**Conclusion**

This project provides a clean, extensible, and assignment-ready solution that meets all requirements of the Pulse Coding Assignment while demonstrating real-world software engineering practices.
