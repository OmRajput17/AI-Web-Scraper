# 🧠 AI Web Scraper

An intelligent web scraping tool that uses LLMs to extract **custom data** from any website based on user instructions — no hardcoded schemas, no manual HTML parsing. Just describe what you want, and get structured JSON/CSV instantly.

---

## 🚀 Features

- 🔍 **Scrape any website** using a simple URL input  
- 🤖 **LLM-powered extraction** — extract *any* type of information (products, prices, tables, FAQs, metadata, etc.)  
- 📦 **Structured output** in both JSON and CSV  
- 💬 **Natural language prompts** — just ask what you want  
- 🧠 Built-in support for **Gemma**, **LLaMA3**, and **Mistral** via Ollama  
- 📥 **Download results** with one click  
- 🧾 **Chat history** to review previous queries  
- 🧹 Clean and readable text content powered by BeautifulSoup and custom cleaning

---

## 🏗️ Tech Stack

- `Python 3.10+`  
- `Streamlit` – UI  
- `Selenium` – DOM scraping  
- `BeautifulSoup` – HTML parsing  
- `LangChain + Ollama` – LLM chat interface  
- `Pandas` – data tabulation and CSV export  

---

## 📦 Project Structure

```
.
├── main.py                         # Streamlit app entry point
├── src/
│   ├── components/
│   │   ├── parser.py              # LLM prompt and logic handler
│   │   └── scraper.py             # Web scraper using Selenium
│   ├── utils/
│   │   └── common.py              # JSON/CSV handlers, content split, cleaning
│   ├── Logging/
│   │   └── logger.py              # Logging configuration
├── output_data/
│   ├── output.json                # Extracted structured data
│   └── output.csv                 # CSV version of the same
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/OmRajput17/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. **Install Dependencies**
   Use a virtual environment (recommended):
   ```bash
   python -m venv ai
   source ai/bin/activate   # or ai\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   streamlit run main.py
   ```

4. **Requirements**
   - [Ollama](https://ollama.com/) must be installed and running
   - Ensure `gemma`, `llama3`, or `mistral` models are available in Ollama
   - `ChromeDriver` must be available in your root folder or PATH

---

## 🧠 How to Use

1. Paste the URL of the website you want to scrape.
2. Click **"Scrape Website"**.
3. Enter a **natural language instruction**, like:
   - "Extract all product names and prices"
   - "Get all customer reviews and ratings"
   - "List job postings and locations"
4. View the structured results and download them as `.json` or `.csv`.

---

## ✅ Output Format

Always returns a clean list of dictionaries:

```json
[
  {
    "brand": "GTPLAYER",
    "price": "₹12,999",
    "rating": "4.3",
    "description": "Ergonomic Gaming Chair with Footrest..."
  }
]
```

---

## 📄 License

This project is open-source and free to use.

---