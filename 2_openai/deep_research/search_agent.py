from openai import AsyncOpenAI
import os
from agents import OpenAIChatCompletionsModel

_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
)
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-3.1-flash-lite",
    openai_client=_client
)
from agents import Agent, ModelSettings, function_tool
from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)
MODEL_NAME = gemini_model

@function_tool
def web_search(query: str) -> str:
    """
    Search the web for the given query term and return the text results.
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', class_='result__snippet')
            snippets = [l.get_text() for l in links[:3]]
            if snippets:
                return '\n\n'.join(snippets)
        return f"Could not retrieve search results for: {query}."
    except Exception as e:
        return f"Search error: {e}"

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [web_search]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=gemini_model, model_settings=settings)