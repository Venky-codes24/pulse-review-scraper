import json
import time
import click
from datetime import datetime

from scraper.g2_scraper import G2Scraper
from scraper.capterra_scraper import CapterraScraper
from scraper.trustradius_scraper import TrustRadiusScraper


def demo_reviews(company: str):
    """
    Return mock reviews for demo/testing purposes
    """
    return [
        {
            "title": "Excellent collaboration tool",
            "review_text": f"{company} has significantly improved our team communication.",
            "date": "2024-03-15",
            "rating": 4.5,
            "source": "demo",
            "reviewer_name": "John D.",
            "reviewer_title": "Product Manager",
            "company_size": "50-200 employees",
            "industry": "Technology",
            "pros": "Easy to use, great integrations",
            "cons": "Can be expensive for large teams",
            "verified_reviewer": True,
            "helpful_count": 12,
            "review_url": "https://example.com/review/1",
            "incentivized": False
        },
        {
            "title": "Good but needs improvement",
            "review_text": f"{company} is reliable but notifications can be noisy.",
            "date": "2024-07-10",
            "rating": 3.8,
            "source": "demo",
            "reviewer_name": "Sarah K.",
            "reviewer_title": "Software Engineer",
            "company_size": "200-500 employees",
            "industry": "IT Services",
            "pros": "Stable platform",
            "cons": "Too many alerts",
            "verified_reviewer": False,
            "helpful_count": 5,
            "review_url": "https://example.com/review/2",
            "incentivized": False
        }
    ]


@click.command()
@click.option("--company", required=True, help="Company name (e.g., Slack)")
@click.option("--start-date", required=False, help="Start date (YYYY-MM-DD)")
@click.option("--end-date", required=False, help="End date (YYYY-MM-DD)")
@click.option(
    "--source",
    default="all",
    help="g2 | capterra | trustradius | all"
)
@click.option(
    "--output",
    default="reviews_output.json",
    help="Output JSON file"
)
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--demo", is_flag=True, help="Run in demo mode with mock data")
def main(company, start_date, end_date, source, output, verbose, demo):
    """
    CLI entry point for SaaS Review Scraper
    """
    start_time = time.time()
    all_reviews = []

    if demo:
        all_reviews = demo_reviews(company)
    else:
        if source in ("g2", "all"):
            g2 = G2Scraper(company, start_date, end_date, verbose)
            all_reviews.extend(g2.scrape())

        if source in ("capterra", "all"):
            capterra = CapterraScraper(company, start_date, end_date, verbose)
            all_reviews.extend(capterra.scrape())

        if source in ("trustradius", "all"):
            tr = TrustRadiusScraper(company, start_date, end_date, verbose)
            all_reviews.extend(tr.scrape())

    result = {
        "metadata": {
            "company_name": company,
            "start_date": start_date,
            "end_date": end_date,
            "source": "demo" if demo else source,
            "total_reviews": len(all_reviews),
            "scrape_date": datetime.utcnow().isoformat(),
            "execution_time_seconds": round(time.time() - start_time, 2)
        },
        "reviews": all_reviews
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Scraping completed. {len(all_reviews)} reviews saved to {output}")


if __name__ == "__main__":
    main()
