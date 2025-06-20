import os
import re
import json
import csv
from datetime import datetime
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Clean extracted HTML text by removing unnecessary whitespace and characters.
    """
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return cleaned

def split_dom_content(dom_content, max_tokens=800):
    """
    Split long DOM content into manageable chunks based on token-like estimation.
    """
    sentences = dom_content.split('.')
    chunks, current_chunk = [], ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_tokens:
            current_chunk += sentence + '.'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '.'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def extract_clean_json(raw_text):
    """
    Extracts and returns a clean list of JSON objects from messy LLM output.
    """
    try:
        match = re.search(r'\[\s*{.*?}\s*\]', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw_text)
    except Exception:
        return []

def save_result_to_json(_, result, output_folder="output_data"):
    """
    Save extracted result as a JSON array (append mode).
    Only stores the structured content, without timestamp or query.
    """
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, "output.json")
    parsed_data = extract_clean_json(result)

    if not parsed_data:
        return filename

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except Exception:
                existing = []
    else:
        existing = []

    combined = existing + parsed_data
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return filename

def save_result_to_csv(_, result, output_folder="output_data"):
    """
    Save structured JSON result into a CSV.
    Only saves keys from JSON objects. No timestamp or query.
    """
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, "output.csv")
    parsed_data = extract_clean_json(result)

    if not parsed_data or not isinstance(parsed_data, list):
        return None

    headers = list(parsed_data[0].keys())
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

    with open(filename, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(headers)

        for item in parsed_data:
            writer.writerow([item.get(h, "") for h in headers])

    return filename
