# main.py

import streamlit as st
from io import StringIO
import json
import pandas as pd
from src.components.scraper import Scraper
from src.components.parser import Parser
from src.Logging.logger import logger
from src.utils.common import save_result_to_json, save_result_to_csv, extract_clean_json

# Page Configuration
st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("🧠 AI Web Scraper")
st.markdown("Enter a website URL to scrape and chat with the content using LLMs.")

# Sidebar Configuration
st.sidebar.title("🔧 Model Settings")

selected_model = st.sidebar.selectbox(
    "Choose LLM Model",
    ["gemma3", "llama3", "mistral"],
    index=0
)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, step=0.05)
top_p = st.sidebar.slider("Top-p (nucleus sampling)", 0.0, 1.0, 0.95, step=0.05)
max_tokens = st.sidebar.slider("Max Tokens", 50, 2048, 512, step=50)

logger.info(f"Using Model: {selected_model}, Temp: {temperature}, Top-p: {top_p}, Max tokens: {max_tokens}")

# Initialize components
scraper = Scraper()
parser = Parser()

# Session State Setup
if "dom_content" not in st.session_state:
    st.session_state["dom_content"] = ""

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# Input: Website URL
url = st.text_input("Website URL")

# Step 1: Scrape Website
if st.button("Scrape Website"):
    if url:
        try:
            st.info("Scraping and cleaning website content...")
            logger.info(f"Scraping requested for: {url}")

            cleaned_content = scraper.get_cleaned_body(url)
            st.session_state["dom_content"] = cleaned_content

            st.success("Website content scraped and cleaned successfully.")
            with st.expander("View Cleaned Content"):
                st.text_area("DOM Content", cleaned_content, height=300)

        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            st.error("Failed to scrape website. Check the URL or try again.")

# Step 2: Chat-Based Interaction
if st.session_state["dom_content"]:
    st.markdown("---")
    st.subheader("💬 Chat About the Website")

    user_query = st.text_input("Ask a question about the content")

    if st.button("Send"):
        if user_query:
            try:
                last_result = st.session_state["conversation"][-1]["response"] if st.session_state["conversation"] else ""

                prompt_with_context = f"""
Previous Result (if any):\n{last_result}\n
Current Instruction:\n{user_query}
"""

                result_chunks = parser.parse(
                    st.session_state["dom_content"],
                    prompt_with_context,
                    model_name=selected_model,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )

                combined_result = "\n".join(result_chunks)

                # Save conversation
                st.session_state["conversation"].append({
                    "query": user_query,
                    "response": combined_result
                })

                # Save output
                json_path = save_result_to_json(combined_result)
                csv_path = save_result_to_csv(combined_result)

                # Display Head of Results
                parsed_data = extract_clean_json(combined_result)
                if parsed_data:
                    df = pd.DataFrame(parsed_data)
                    st.markdown("### 📄 Preview Extracted Results")
                    st.dataframe(df.head(), use_container_width=True)

                    with open(json_path, "r", encoding="utf-8") as jf:
                        st.download_button("📥 Download JSON", jf.read(), file_name="output.json")
                    with open(csv_path, "r", encoding="utf-8") as cf:
                        st.download_button("📥 Download CSV", cf.read(), file_name="output.csv")
                else:
                    st.info("No structured data to show.")

            except Exception as e:
                logger.error(f"Parsing failed: {e}")
                st.error("Failed to parse content. Try again.")

# Step 3: Display Chat History
if st.session_state["conversation"]:
    st.markdown("### 🧾 Conversation History")
    for i, entry in enumerate(reversed(st.session_state["conversation"])):
        st.markdown(f"**🧑‍💻 You:** {entry['query']}")
        st.markdown(f"**🤖 AI:**")
        st.code(entry["response"], language="text")

    if st.button("Clear Chat History"):
        st.session_state["conversation"] = []
        st.success("Conversation cleared.")
