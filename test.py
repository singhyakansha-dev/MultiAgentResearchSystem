import streamlit as st
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

st.set_page_config(page_title="ResearchMind", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

for key, default in {"results": {}, "running": False, "finished": False, "topic": ""}.items():
    st.session_state.setdefault(key, default)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@300;400;500;600&display=swap');
html, body, [class*="css"]{ font-family:'Rajdhani',sans-serif; }
.stApp{
    background:#070811;
    background-image: radial-gradient(circle at top left,#401060 0%,transparent 40%),
                       radial-gradient(circle at bottom right,#00384d 0%,transparent 35%);
    color:white;
}
.block-container{ padding-top:2rem; padding-bottom:3rem; max-width:1350px; }
#MainMenu, footer, header{ visibility:hidden; }
.hero{ padding:40px; border-radius:24px; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); backdrop-filter:blur(18px); margin-bottom:30px; }
.hero_small{ color:#00E5FF; letter-spacing:4px; font-size:13px; text-transform:uppercase; font-weight:700; }
.hero_title{ font-family:Orbitron; font-size:58px; font-weight:800; margin-top:10px; }
.hero_title span{ color:#00E5FF; }
.hero_desc{ font-size:20px; color:#B5C6D6; margin-top:15px; line-height:1.7; }
.card{ background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:25px; backdrop-filter:blur(18px); }
.step{ padding:18px; border-radius:14px; background:#101622; margin-bottom:15px; border-left:5px solid #333; }
.waiting{ border-left-color:#777; }
.running{ border-left-color:#00E5FF; box-shadow:0 0 20px rgba(0,229,255,.35); }
.done{ border-left-color:#00FF99; }
.stButton>button{ width:100%; height:55px; border-radius:12px; border:none; background:linear-gradient(135deg,#00E5FF,#9A5BFF); color:white; font-weight:700; font-size:17px; }
.stButton>button:hover{ transform:translateY(-2px); }
.stTextInput input{ border-radius:12px !important; background:#141A28 !important; color:white !important; }
.report{ background:#0E1422; border-radius:18px; padding:30px; border:1px solid rgba(255,255,255,.08); }
.footer{ text-align:center; margin-top:50px; color:#7B8BA3; }
</style>
""", unsafe_allow_html=True)

STEPS = ["Search Agent", "Reader Agent", "Writer Agent", "Critic Agent"]
DESCS = {
    "waiting": ["Searches trusted web sources.", "Reads and extracts webpage content.",
                "Creates a detailed research report.", "Reviews and scores the report."],
    "running": ["Searching trusted sources...", "Reading webpages...", "Generating report...", "Reviewing..."],
    "done": ["Completed"] * 4,
}
ICONS = {"waiting": "⚪", "running": "🔄", "done": "✅"}
text_of = lambda x: x.content if hasattr(x, "content") else str(x)


def render_pipeline(active_idx=-1):
    """active_idx: index of running step, or 4 for all-done, or -1 for all-waiting."""
    html = ""
    for i, name in enumerate(STEPS):
        state = "done" if i < active_idx or active_idx == 4 else "running" if i == active_idx else "waiting"
        desc = DESCS[state][i] if state != "waiting" or active_idx == -1 else DESCS["waiting"][i]
        html += f'<div class="step {state}">\n\n### {ICONS[state]} {name}\n\n{desc}\n\n</div>\n'
    pipeline_placeholder.markdown(html, unsafe_allow_html=True)


st.markdown("""
<div class="hero">
<div class="hero_small">MULTI AGENT AI RESEARCH SYSTEM</div>
<div class="hero_title">Research<span>Mind</span></div>
<div class="hero_desc">Four specialized AI agents collaborate to search the web,
read trusted sources, generate an in-depth report, and critically review the final output.</div>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([2.2, 1], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Research Topic")
    topic = st.text_input("", placeholder="Example: Future of Quantum Computing",
                           value=st.session_state.topic, key="topic_input", label_visibility="collapsed")
    st.session_state.topic = topic
    generate = st.button("🚀 Generate Research Report", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 💡 Suggested Topics")
    topics = ["LLM Agents in 2026", "Artificial General Intelligence", "SpaceX Starship",
              "Fusion Energy", "Brain Computer Interfaces", "Quantum Internet"]
    col1, col2 = st.columns(2)
    for i, t in enumerate(topics):
        (col1 if i % 2 == 0 else col2).info(t)

with right_col:
    st.markdown("## ⚙ Pipeline Status")
    pipeline_placeholder = st.empty()
    render_pipeline(-1)

progress_bar = st.progress(0)
status_text = st.empty()

if generate:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.session_state.update(running=True, finished=False, results={})
        results = {}
        stage_msgs = ["🔍 Search Agent is searching...", "📄 Reader Agent is reading sources...",
                      "✍ Writer Agent is writing report...", "🧐 Critic Agent is reviewing report..."]
        progress_vals = [10, 30, 55, 80]

        status_text.info(stage_msgs[0]); render_pipeline(0)
        search_result = build_search_agent().invoke({"messages": [
            ("user", f"Find recent, reliable and detailed information about {topic}")]})
        results["search"] = search_result["messages"][-1].content
        progress_bar.progress(progress_vals[0])

        status_text.info(stage_msgs[1]); render_pipeline(1)
        reader_result = build_reader_agent().invoke({"messages": [
            ("user", f"Use the search results below.\n\nChoose the best URL.\n\nUse scrape_url.\n\n"
                     f"Search Results:\n\n{results['search']}")]})
        results["reader"] = reader_result["messages"][-1].content
        progress_bar.progress(progress_vals[1])

        status_text.info(stage_msgs[2]); render_pipeline(2)
        research = (f"\nSEARCH RESULTS\n\n{results['search']}\n\n"
                    f"--------------------------------------------\n\nSCRAPED CONTENT\n\n{results['reader']}\n")
        results["report"] = writer_chain.invoke({"topic": topic, "research": research})
        progress_bar.progress(progress_vals[2])

        status_text.info(stage_msgs[3]); render_pipeline(3)
        results["feedback"] = critic_chain.invoke({"report": results["report"]})
        progress_bar.progress(100)
        status_text.success("✅ Research Completed")
        render_pipeline(4)

        st.session_state.results = results
        st.session_state.finished = True
        st.session_state.running = False

if st.session_state.finished:
    st.markdown("---")
    st.header("📄 Research Report")
    report_text = text_of(st.session_state.results.get("report", ""))
    st.markdown(f'<div class="report">\n\n{report_text}\n\n</div>', unsafe_allow_html=True)

    st.header("🧐 Critic Feedback")
    st.info(text_of(st.session_state.results.get("feedback", "")))

    with st.expander("🔍 Search Agent Output"):
        st.write(text_of(st.session_state.results.get("search", "")))
    with st.expander("📄 Reader Agent Output"):
        st.write(text_of(st.session_state.results.get("reader", "")))

    col1, col2 = st.columns(2)
    for col, ext, mime in [(col1, "md", "text/markdown"), (col2, "txt", "text/plain")]:
        col.download_button(f"⬇ Download Report (.{ext})", data=report_text,
                             file_name=f"{topic.replace(' ', '_')}_report.{ext}", mime=mime,
                             use_container_width=True)

    if st.button("🔄 Start New Research", use_container_width=True):
        st.session_state.update(finished=False, running=False, results={})
        st.rerun()

st.markdown("""
<div class="footer">
ResearchMind • Multi-Agent AI Research System<br>
Powered by LangChain • Mistral • Tavily • Streamlit
</div>
""", unsafe_allow_html=True)