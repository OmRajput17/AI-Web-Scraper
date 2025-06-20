import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "ai_web_scraper"

# Define the full folder/file structure
list_of_files = [
    f"main.py",
    f"requirements.txt",
    f"README.md",
    f".gitignore",
    
    f"utils/__init__.py",
    f"utils/cleaner.py",
    
    f"Logging/__init__.py",
    f"Logging/logger.py",

    f"logs/.gitkeep" 
]

# Create folders and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory created: {filedir}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Empty file created: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
