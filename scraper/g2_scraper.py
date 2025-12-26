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


class G2Scraper(BaseScraper):
    """
    Scraper implementation for G2 reviews.
    """

    BASE_URL = "https://www.g2.com/products/{product}/reviews"

    def scrape(self) -> List[Dict]:
        reviews: List[Dict] = []
        page = 1

        self.log_info(f"Starting G2 scrape for {self.company_name}")

        while True:
            product_slug = self.company_name.lower().replace(" ", "-")
            url = f"{self.BASE_URL.format(product=product_slug)}?page={page}"

            headers = {
                "User-Agent": get_random_user_agent(),
                "Accept-Language": "en-US,en;q=0.9"
            }

            try:
                response = requests.get(url, headers=headers, timeout=20)
            except requests.RequestException as exc:
                self.log_error(f"Request failed: {exc}")
                break

            if response.status_code != 200:
                self.log_warning(f"Non-200 status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, "lxml")
            review_blocks = soup.select("div.review")

            # Stop if no more reviews (pagination end)
            if not review_blocks:
                self.log_info("No more reviews found on G2")
                break

            for block in review_blocks:
                try:
                    title_tag = block.select_one(".review-title")
                    body_tag = block.select_one(".review-body")
                    date_tag = block.select_one(".date")

                    if not (title_tag and body_tag and date_tag):
                        continue

                    parsed_date = parse_date_safe(date_tag.text)
                    if not parsed_date:
                        continue

                    # Date filtering
                    if not is_date_in_range(
                        parsed_date,
                        self.start_date,
                        self.end_date
                    ):
                        continue

                    rating_value = block.get("data-rating", 0)

                    review = {
                        "title": title_tag.text.strip(),
                        "review_text": body_tag.text.strip(),
                        "date": parsed_date,
                        "rating": normalize_rating(rating_value),
                        "source": "g2",
                        "reviewer_name": None,
                        "reviewer_title": None,
                        "company_size": None,
                        "industry": None,
                        "pros": None,
                        "cons": None,
                        "verified_reviewer": "Verified" in block.text,
                        "helpful_count": None,
                        "review_url": url,
                        "incentivized": False
                    }

                    reviews.append(review)

                except Exception as exc:
                    self.log_warning(f"Failed to parse a review: {exc}")
                    continue

            random_delay()
            page += 1

        self.log_info(f"G2 scrape completed. Reviews collected: {len(reviews)}")
        return reviews
