import requests
from typing import List, Dict
from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import parse_date_safe, is_date_in_range, normalize_rating


class TrustRadiusScraper(BaseScraper):
    """
    Scraper implementation for TrustRadius reviews
    """

    BASE_URL = "https://www.trustradius.com/products/{product}/reviews"

    def scrape(self) -> List[Dict]:
        reviews: List[Dict] = []

        slug = self.company_name.lower().replace(" ", "-")
        url = self.BASE_URL.format(product=slug)

        try:
            response = requests.get(url, timeout=20)
        except requests.RequestException:
            return reviews

        if response.status_code != 200:
            return reviews

        soup = BeautifulSoup(response.text, "lxml")
        blocks = soup.select("div.review")

        for block in blocks:
            body = block.select_one("p")
            date_tag = block.select_one("time")

            if not (body and date_tag):
                continue

            date = parse_date_safe(date_tag.get("datetime", ""))
            if not date or not is_date_in_range(date, self.start_date, self.end_date):
                continue

            reviews.append({
                "title": "TrustRadius Review",
                "review_text": body.text.strip(),
                "date": date,
                "rating": normalize_rating(0),
                "source": "trustradius",
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
            })

        return reviews
