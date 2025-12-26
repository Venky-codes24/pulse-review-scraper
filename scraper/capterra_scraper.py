import requests
from typing import List, Dict
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import (
    random_delay,
    get_random_user_agent,
    parse_date_safe,
    is_date_in_range,
    normalize_rating
)


class CapterraScraper(BaseScraper):
    """
    Scraper implementation for Capterra reviews.

    NOTE:
    Capterra has strong bot protection.
    This implementation focuses on clean architecture
    and graceful handling rather than aggressive scraping.
    """

    BASE_URL = "https://www.capterra.com/p/{product}/reviews/"

    def scrape(self) -> List[Dict]:
        reviews: List[Dict] = []

        self.log_info(f"Starting Capterra scrape for {self.company_name}")

        product_slug = self.company_name.lower().replace(" ", "-")
        url = self.BASE_URL.format(product=product_slug)

        headers = {
            "User-Agent": get_random_user_agent(),
            "Accept-Language": "en-US,en;q=0.9"
        }

        try:
            response = requests.get(url, headers=headers, timeout=20)
        except requests.RequestException as exc:
            self.log_error(f"Capterra request failed: {exc}")
            return reviews

        if response.status_code != 200:
            self.log_warning(
                f"Capterra returned status code {response.status_code}"
            )
            return reviews

        soup = BeautifulSoup(response.text, "lxml")
        review_blocks = soup.select("div.review")

        if not review_blocks:
            self.log_warning(
                "No reviews found or page blocked by Capterra"
            )
            return reviews

        for block in review_blocks:
            try:
                title_tag = block.select_one(".review-title")
                body_tag = block.select_one(".review-text")
                date_tag = block.select_one("time")

                if not (title_tag and body_tag and date_tag):
                    continue

                parsed_date = parse_date_safe(
                    date_tag.get("datetime", "")
                )

                if not parsed_date:
                    continue

                if not is_date_in_range(
                    parsed_date,
                    self.start_date,
                    self.end_date
                ):
                    continue

                rating_tag = block.select_one(".rating")

                rating_value = (
                    rating_tag.text.strip()
                    if rating_tag else 0
                )

                review = {
                    "title": title_tag.text.strip(),
                    "review_text": body_tag.text.strip(),
                    "date": parsed_date,
                    "rating": normalize_rating(rating_value),
                    "source": "capterra",
                    "reviewer_name": None,
                    "reviewer_title": None,
                    "company_size": None,
                    "industry": None,
                    "pros": None,
                    "cons": None,
                    "verified_reviewer": False,
                    "helpful_count": None,
                    "review_url": url,
                    "incentivized": False
                }

                reviews.append(review)

            except Exception as exc:
                self.log_warning(
                    f"Failed to parse Capterra review: {exc}"
                )
                continue

        random_delay()
        self.log_info(
            f"Capterra scrape completed. Reviews collected: {len(reviews)}"
        )
        return reviews
