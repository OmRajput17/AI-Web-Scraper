# src/components/parser.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from src.utils.common import split_dom_content
from src.Logging.logger import logger

class Parser:
    def __init__(self):
        # General-purpose, instruction-following prompt template
        self.template = (
            "You are an intelligent extraction agent.\n"
            "You will receive a chunk of website text content and a specific instruction from the user.\n\n"
            "Your ONLY job is to extract relevant data as per the user's instruction.\n\n"
            "TEXT CONTENT:\n{dom_content}\n\n"
            "INSTRUCTION:\n{parse_description}\n\n"
            "📌 STRICT RULES TO FOLLOW:\n"
            "1. ✅ Only extract data strictly matching the instruction.\n"
            "2. 🚫 Do not add explanations, comments, or formatting like markdown.\n"
            "3. ⛔ Do not hallucinate or guess — skip irrelevant info.\n"
            "4. 🔒 If nothing relevant is found, return an empty string: ''\n"
            "5. 📄 If structured output is possible, return it as a clean JSON list of dictionaries.\n"
            "6. 🧮 The keys of the dictionary should be derived from the user's instruction.\n"
            "7. 📦 Avoid including raw HTML, CSS, or JavaScript content.\n"
        )

    def parse(self, dom_content, parse_description,
              model_name="gemma", temperature=0.7, top_p=0.95, max_tokens=512):
        """
        Public method to parse the website content using the provided instruction.
        """
        dom_chunks = split_dom_content(dom_content)
        return self.parse_with_ollama(dom_chunks, parse_description, model_name,
                                      temperature, top_p, max_tokens)

    def parse_with_ollama(self, dom_chunks, parse_description,
                          model_name="gemma", temperature=0.7, top_p=0.95, max_tokens=512):
        """
        Internal function that runs LangChain-Ollama pipeline chunk-by-chunk.
        """
        prompt = ChatPromptTemplate.from_template(self.template)
        model = OllamaLLM(
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        chain = prompt | model

        parsed_results = []
        total_batches = len(dom_chunks)

        for i, chunk in enumerate(dom_chunks, start=1):
            logger.info(f"Processing batch {i} of {total_batches}")
            try:
                response = chain.invoke({
                    "dom_content": chunk,
                    "parse_description": parse_description
                })
                parsed_results.append(response)
            except Exception as e:
                logger.error(f"Batch {i} failed: {e}")
                continue

        return "\n".join(parsed_results)
