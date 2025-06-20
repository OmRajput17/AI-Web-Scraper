# src/utils/cleaner.py

from bs4 import BeautifulSoup
import logging

"""
Utility functions for cleaning and splitting HTML body content.
These functions are used after scraping the website.
"""

def clean_body_content(body_content: str) -> str:
    """
    Cleans HTML body content by removing non-visible elements like
    <script> and <style>, and returns only human-readable text.

    Args:
        body_content (str): Raw HTML string from the <body> tag.

    Returns:
        str: Cleaned, readable text content.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text and normalize line spacing
    cleaned_text = soup.get_text(separator="\n")
    cleaned_text = "\n".join(
        line.strip() for line in cleaned_text.splitlines() if line.strip()
    )

    logging.info("DOM content cleaned and formatted.")
    return cleaned_text


def split_dom_content(dom_content: str, max_length: int = 6000) -> list:
    """
    Splits cleaned text content into smaller chunks for LLM parsing.

    Args:
        dom_content (str): Cleaned DOM content.
        max_length (int): Max characters per chunk (default: 6000).

    Returns:
        list: List of text chunks.
    """
    chunks = [
        dom_content[i: i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]

    logging.info(f"DOM content split into {len(chunks)} chunks.")
    return chunks
