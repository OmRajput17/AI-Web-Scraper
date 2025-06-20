# src/components/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from src.utils.cleaner import clean_body_content
from src.Logging.logger import logger


class Scraper:
    """
    Scraper class to handle automated website data extraction
    using Selenium and BeautifulSoup.
    """

    def __init__(self, chrome_driver_path: str = "./chromedriver.exe", headless: bool = False):
        """
        Initializes the Selenium Chrome driver.

        Args:
            chrome_driver_path (str): Path to chromedriver executable.
            headless (bool): Whether to run the browser in headless mode.
        """
        self.chrome_driver_path = chrome_driver_path
        self.options = webdriver.ChromeOptions()
        if headless:
            # self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.options.add_argument("--log-level=3")  # Suppress unnecessary logs

    def scrape_website(self, url: str) -> str:
        """
        Loads the webpage and extracts raw HTML content.

        Args:
            url (str): Website URL to scrape.

        Returns:
            str: Raw HTML content of the loaded page.
        """
        logger.info(f"Launching browser to scrape: {url}")
        driver = None

        try:
            driver = webdriver.Chrome(
                service=Service(self.chrome_driver_path),
                options=self.options
            )
            driver.get(url)
            logger.info("Website loaded successfully.")
            html = driver.page_source
            return html

        except Exception as e:
            logger.error(f"Failed to load website: {e}")
            raise e

        finally:
            if driver:
                driver.quit()
                logger.info("Browser closed.")

    def extract_body_content(self, html_content: str) -> str:
        """
        Extracts the <body> content from the given HTML.

        Args:
            html_content (str): Full HTML source.

        Returns:
            str: HTML body content as string.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body

        if body_content:
            logger.info("Body content extracted successfully.")
            return str(body_content)

        logger.warning("No <body> tag found in the HTML content.")
        return ""

    def get_cleaned_body(self, url: str) -> str:
        """
        Full pipeline: scrape the website, extract <body>, clean content.

        Args:
            url (str): Website to scrape.

        Returns:
            str: Cleaned, readable content from the site.
        """
        html = self.scrape_website(url)
        raw_body = self.extract_body_content(html)
        cleaned = clean_body_content(raw_body)

        logger.info("Cleaned body content generated.")
        return cleaned
