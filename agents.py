from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

import os

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

llm = ChatMistralAI(
    api_key=api_key,
    model="mistral-small-2506",
    temperature=0,
)

# -------------------------
# Model
# -------------------------

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a research search agent.

Always use the web_search tool to answer the user's request.

Never answer from your own knowledge.
Return all relevant URLs and snippets.
"""
    )
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a web reading agent.

Always use the scrape_url tool.

Choose the most relevant URL and scrape it.

Return only the extracted content.
"""
    )
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
"""
    )
])
writer_chain = writer_prompt | llm | StrOutputParser()
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict research reviewer."
    ),
    (
        "human",
        """
Review this report.

{report}

Return

Score: X/10

Strengths

Areas to Improve

Verdict
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()