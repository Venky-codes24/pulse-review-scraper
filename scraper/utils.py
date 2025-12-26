import random
import time
from datetime import datetime
from typing import Optional

from dateutil.parser import parse
from fake_useragent import UserAgent

# Initialize UserAgent once
_user_agent = UserAgent()


def random_delay(min_delay: float = 2.0, max_delay: float = 3.0) -> None:
    """
    Sleep for a random duration between min_delay and max_delay.
    Used for rate limiting to avoid blocking.
    """
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def get_random_user_agent() -> str:
    """
    Return a random User-Agent string.
    """
    return _user_agent.random


def parse_date_safe(date_text: str) -> Optional[str]:
    """
    Safely parse a date string and return it in YYYY-MM-DD format.
    Returns None if parsing fails.
    """
    try:
        parsed_date = parse(date_text, fuzzy=True)
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        return None


def is_date_in_range(
    date_str: str,
    start_date: str,
    end_date: str
) -> bool:
    """
    Check if date_str is within start_date and end_date (inclusive).
    All dates must be in YYYY-MM-DD format.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= date <= end
    except Exception:
        return False


def normalize_rating(rating: float, max_scale: float = 5.0) -> float:
    """
    Normalize rating to a fixed scale (default: 5.0).
    """
    try:
        rating = float(rating)
        return round(min(max(rating, 0.0), max_scale), 2)
    except Exception:
        return 0.0
