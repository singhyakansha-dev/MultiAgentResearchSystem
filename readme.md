#  ResearchMind – Multi-Agent AI Research System

ResearchMind is a Streamlit-based AI research assistant that uses multiple specialized AI agents to collaboratively perform web research, summarize information, generate comprehensive reports, and review the final output.

The application demonstrates how multiple LLM-powered agents can work together in a sequential workflow to automate the research process.

##  Features

- 🔍 AI Search Agent for finding relevant web information
- 📄 Reader Agent for extracting webpage content
- ✍️ Writer Agent for generating structured research reports
- 🧐 Critic Agent for evaluating and improving report quality
- 📊 Interactive Streamlit dashboard
- ⚡ Live pipeline progress visualization
- 📥 Download generated reports
- 🎨 Modern cyberpunk-inspired UI

##  System Architecture

```
              User Query
                   │
                   ▼
          Search Agent (Tavily)
                   │
                   ▼
          Reader Agent (Web Scraper)
                   │
                   ▼
         Writer Agent (Mistral LLM)
                   │
                   ▼
         Critic Agent (LLM Review)
                   │
                   ▼
          Final Research Report
```

##  Project Structure

```
ResearchMind/

│── app.py
│── agents.py
│── pipeline.py
│── tools.py
│── requirements.txt
│── README.md
│── .env

```

##  Technologies Used

### Frontend
- Streamlit

### Backend
- Python

### AI Framework
- LangChain

### LLM
- Mistral AI

### Search Engine
- Tavily Search API

### Web Scraping
- BeautifulSoup
- Requests

### Environment Management
- Python Dotenv

##  Workflow

1. User enters a research topic.
2. Search Agent searches trusted web sources.
3. Reader Agent extracts webpage content.
4. Writer Agent generates a detailed research report.
5. Critic Agent reviews and evaluates the report.
6. Final report is displayed and available for download.

##  Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ResearchMind.git
```

Navigate into the project

```bash
cd ResearchMind
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

##  Environment Variables

Create a `.env` file in the root directory.

```env
MISTRAL_API_KEY=your_mistral_api_key

TAVILY_API_KEY=your_tavily_api_key
```

## ▶ Run the Application

```bash
streamlit run app.py
```

##  Screenshots

Add screenshots of:

- Home page
- Pipeline execution
- Final report
- Critic feedback

##  Future Improvements

- Multi-source research
- PDF export
- Citation generation
- Research history
- Report editing
- RAG integration
- Memory for agents
- Parallel agent execution
- Local LLM support
- Authentication

##  Skills Demonstrated

- Multi-Agent AI Systems
- Generative AI
- LangChain
- LLM Prompt Engineering
- Web Scraping
- API Integration
- Streamlit Development
- Python
- State Management
- UI Design

##  Author

**Yakansha Singh**

LinkedIn: linkedin.com/in/yakansha-singh-dev 

GitHub:  github.com/singhyakansha-dev
