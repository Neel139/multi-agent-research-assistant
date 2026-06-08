# Multi-Agent Research Assistant

An agentic AI system where 4 specialized LLM agents collaborate to research any topic and produce a structured, fact-checked report — fully automated from a single query.

Built with Groq LLaMA 3.3-70b, Tavily Search, LangChain, and Streamlit.

---

## How It Works

A user types a research query. The **Orchestrator** breaks it into focused sub-queries and routes them to 4 specialist agents in sequence:

```
User Query
    │
    ▼
Orchestrator — plans 2-3 search queries
    │
    ├── 🔍 Search Agent      — finds real web sources via Tavily
    ├── 📝 Summarizer Agent  — condenses sources into key findings  
    ├── ✅ Fact-checker Agent — validates claims, flags gaps
    └── ✍️  Writer Agent      — produces final structured report
    │
    ▼
Final Research Report (Markdown)
```

---

## Demo

Type any research question:
- *"What are the latest breakthroughs in agentic AI in 2025?"*
- *"How does retrieval-augmented generation work?"*
- *"What caused the 2008 financial crisis?"*

The system searches the web in real time, summarizes findings, fact-checks them, and writes a full report with cited sources — in under 60 seconds.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq LLaMA 3.3-70b-versatile (free tier) |
| Web search | Tavily Search API (free tier) |
| Agent framework | LangChain |
| UI | Streamlit |
| Tunneling (Colab) | pyngrok |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Neel139/multi-agent-research-assistant
cd multi-agent-research-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set API keys**

Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

```
GROQ_API_KEY=your_groq_key        # free at groq.com
TAVILY_API_KEY=your_tavily_key    # free at tavily.com
```

**4. Run**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Run on Google Colab

Open the notebook, set your API keys in Cell 2, and run all cells. A public ngrok URL will be generated automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1McIZcoxYSfUFfvKSjxTMiYkibzZvnIgc?usp=sharing)

---

## Agent Details

**Orchestrator** — receives the user query, uses the LLM to decompose it into 2-3 targeted search queries, then coordinates all agents in sequence and aggregates their outputs.

**Search Agent** — calls the Tavily Search API with `search_depth="advanced"` to retrieve up to 5 high-quality sources per query. Deduplicates by URL across multiple searches.

**Summarizer Agent** — takes all retrieved source content and instructs the LLM to extract and condense the key findings relevant to the original query.

**Fact-checker Agent** — reviews the summary against the source list, identifies unsupported or questionable claims, and flags important nuances or missing context.

**Writer Agent** — takes the summary and fact-check notes and produces a fully structured Markdown report with Overview, Key Findings, Analysis, Conclusion, and cited Sources sections.

---

## Project Structure

```
multi-agent-research-assistant/
├── app.py               # Main Streamlit app + all agents
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── .gitignore
└── README.md
```

---

## Key Concepts Demonstrated

- **Agentic AI** — multiple LLM agents with distinct roles collaborating on a shared task
- **Prompt engineering** — structured prompts with role definitions and output formatting for each agent
- **LLM orchestration** — an orchestrator agent that plans, delegates, and aggregates
- **Tool use** — agents calling external APIs (Tavily) as tools
- **RAG-adjacent retrieval** — live web retrieval feeding LLM context at inference time
