from abc import ABC, abstractmethod
from typing import List, Dict
from loguru import logger


class BaseScraper(ABC):
    """
    Abstract base class for all review scrapers.
    Every platform scraper must inherit from this class.
    """

    def __init__(
        self,
        company_name: str,
        start_date: str,
        end_date: str,
        verbose: bool = False
    ) -> None:
        self.company_name = company_name
        self.start_date = start_date
        self.end_date = end_date
        self.verbose = verbose

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape reviews from a specific platform.
        Must be implemented by child classes.
        """
        pass

    def log_info(self, message: str) -> None:
        if self.verbose:
            logger.info(message)

    def log_warning(self, message: str) -> None:
        logger.warning(message)

    def log_error(self, message: str) -> None:
        logger.error(message)
