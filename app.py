
import streamlit as st
import os
import ast
from langchain_groq import ChatGroq
from tavily import TavilyClient

# ── Init ──────────────────────────────────────────────────
groq_key   = os.environ.get("GROQ_API_KEY")
tavily_key = os.environ.get("TAVILY_API_KEY")

if not groq_key or not tavily_key:
    st.error("Missing API keys. Set GROQ_API_KEY and TAVILY_API_KEY as environment variables.")
    st.stop()

llm    = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
tavily = TavilyClient(tavily_key)

# ── Agents ────────────────────────────────────────────────
def search_agent(query):
    results = tavily.search(query=query, max_results=5, search_depth="advanced")
    return [{"title": r["title"], "url": r["url"], "content": r["content"]}
            for r in results["results"]]

def summarizer_agent(sources, query):
    combined = "\n\n".join([f"Source: {s['title']}\n{s['content']}" for s in sources])
    prompt = f"""You are a research summarizer. Summarize key findings about "{query}".
SOURCES:\n{combined}\nSUMMARY:"""
    return llm.invoke(prompt).content

def factchecker_agent(summary, sources):
    source_titles = "\n".join([f"- {s['title']} ({s['url']})" for s in sources])
    prompt = f"""You are a fact-checker. Review this summary for unsupported claims.
SOURCES:\n{source_titles}\nSUMMARY:\n{summary}\nFACT-CHECK REPORT:"""
    return llm.invoke(prompt).content

def writer_agent(query, summary, factcheck, sources):
    source_list = "\n".join([f"- [{s['title']}]({s['url']})" for s in sources])
    prompt = f"""Write a comprehensive research report on: "{query}"
Use this summary: {summary}
Consider these fact-check notes: {factcheck}
Format with: # Title, ## Overview, ## Key Findings, ## Analysis, ## Conclusion, ## Sources
Cite these sources:\n{source_list}"""
    return llm.invoke(prompt).content

def orchestrator(query):
    plan_prompt = f"""Break "{query}" into 2-3 focused search queries.
Return ONLY a Python list of strings, nothing else.
Example: ["query 1", "query 2"]"""
    try:
        queries = ast.literal_eval(llm.invoke(plan_prompt).content.strip())
    except:
        queries = [query]

    all_sources = []
    for q in queries:
        all_sources.extend(search_agent(q))

    seen, unique = set(), []
    for s in all_sources:
        if s["url"] not in seen:
            seen.add(s["url"])
            unique.append(s)

    summary   = summarizer_agent(unique, query)
    factcheck = factchecker_agent(summary, unique)
    report    = writer_agent(query, summary, factcheck, unique)

    return {
        "queries":   queries,
        "sources":   unique,
        "summary":   summary,
        "factcheck": factcheck,
        "report":    report
    }

# ── UI ────────────────────────────────────────────────────
st.set_page_config(page_title="Multi-Agent Research Assistant", 
                   page_icon="🔬", layout="wide")

st.title("🔬 Multi-Agent Research Assistant")
st.caption("Powered by Groq LLaMA 3.3-70b · Tavily Search · LangChain · 4 AI agents collaborating")

st.markdown("""
| Agent | Role |
|-------|------|
| 🔍 Search | Finds relevant web sources |
| 📝 Summarizer | Condenses content into key findings |
| ✅ Fact-checker | Validates claims and flags gaps |
| ✍️ Writer | Produces the final structured report |
""")

st.markdown("---")

query = st.text_input("What do you want to research?",
                       placeholder="e.g. What are the latest breakthroughs in agentic AI in 2025?")

if st.button("🚀 Start Research", type="primary") and query:

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.status("Agents working...", expanded=True) as status:
            st.write("📋 Orchestrator planning research queries...")
            result = orchestrator(query)
            st.write("🔍 Search agent found sources...")
            st.write("📝 Summarizer condensed findings...")
            st.write("✅ Fact-checker reviewed claims...")
            st.write("✍️ Writer produced final report...")
            status.update(label="✅ Research complete!", state="complete")

        st.markdown("---")
        st.markdown(result["report"])

    with col2:
        st.subheader("🔍 Search queries")
        for q in result["queries"]:
            st.code(q)

        st.subheader("📚 Sources")
        for s in result["sources"][:8]:
            st.markdown(f"- [{s['title']}]({s['url']})")

        with st.expander("✅ Fact-check notes"):
            st.write(result["factcheck"])

        with st.expander("📝 Raw summary"):
            st.write(result["summary"])
