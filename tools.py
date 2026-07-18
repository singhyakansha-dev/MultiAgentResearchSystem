from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests, os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY not found in .env file")


@tool
def web_search(query: str) -> str:
    """Search the web and return titles, URLs and snippets."""
    try:
        results = tavily.search(query=query, max_results=5).get("results", [])

        if not results:
            return "No search results found."

        return "\n" + "-" * 80 + "\n".join(
            f"\nTitle: {r.get('title','N/A')}"
            f"\nURL: {r.get('url','N/A')}"
            f"\nSnippet:\n{r.get('content','No content available')[:300]}"
            for r in results
        )

    except Exception as e:
        return f"Web search failed: {e}"


@tool
def scrape_url(url: str) -> str:
    """Scrape readable text from a webpage."""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        return " ".join(soup.get_text(" ", strip=True).split())[:3000]

    except requests.exceptions.RequestException as e:
        return f"Could not scrape URL: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
