import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from engine.coordinator import CoordinatorAgent

# Load dotenv config
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Phishing Forensics Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS for Cyber Dark Theme
st.markdown("""
<style>
    /* Dark Cyber Theme Background & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d0f12;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #12161a !important;
        border-right: 1px solid #1f2937;
    }
    
    /* Header and Subtitles */
    h1, h2, h3 {
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    .main-title {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        font-weight: 800;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphic Container Cards */
    .glass-card {
        background: rgba(22, 28, 36, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    
    /* Glowing Threat Score Badge */
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        border-radius: 50%;
        width: 180px;
        height: 180px;
        margin: 0 auto 20px auto;
        border: 4px solid #10b981;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
    }
    
    .score-critical {
        border-color: #ef4444 !important;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4) !important;
    }
    
    .score-warning {
        border-color: #f59e0b !important;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.3) !important;
    }
    
    .score-num {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Fira Code', monospace;
    }
    
    .score-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
    }
    
    /* Retro Glowing Hacker Terminal */
    .terminal-container {
        background-color: #05070a;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Fira Code', monospace;
        color: #22c55e;
        box-shadow: inset 0 0 10px rgba(34, 197, 94, 0.15), 0 0 15px rgba(0, 0, 0, 0.5);
        height: 250px;
        overflow-y: auto;
        margin-bottom: 25px;
    }
    
    .terminal-line {
        line-height: 1.6;
        margin-bottom: 6px;
    }
    
    /* Input Styling */
    .stTextInput input {
        background-color: #121820 !important;
        border: 1px solid #1e293b !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45) !important;
    }
    
    /* Sidebar info */
    .sidebar-info {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("<div class='main-title'>🛡️ MULTI-AGENT PHISHING FORENSICS ENGINE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Autonomous Multi-Agent Collaboration for Deep Suspicious Link Auditing</div>", unsafe_allow_html=True)

# Sidebar setup
st.sidebar.image("https://img.icons8.com/nolan/128/security-shield.png", width=80)
st.sidebar.markdown("### ⚙️ Engine Settings")

# Check environment for Gemini API Key, fallback to empty
default_api_key = os.getenv("GEMINI_API_KEY") or ""
api_key_input = st.sidebar.text_input("Gemini API Key", value=default_api_key, type="password", help="Needed for multimodal visual and deep AI code reasoning.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Collaborative AI Roster")
st.sidebar.markdown("""
- **🕵️‍♂️ Coordinator Agent:** Manages agent flow and orchestrates state transitions.
- **🌐 Scraper Agent:** Navigates via headless Playwright, extracts full DOM, and captures snapshots.
- **💻 Code Analyst Agent:** Reviews source logic for hex code obfuscation and input capture action domains.
- **🎨 Reporter Agent:** Audits visual deception layouts using Gemini Vision and constructs reports.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Sample Links")
st.sidebar.markdown("""
Try scanning these links:
- `google.com` (Safe brand example)
- `wikipedia.org` (Safe reference example)
- `github.com` (Safe repository example)
""")

# Input section
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
url_to_scan = st.text_input("Enter Suspect URL to Investigate", placeholder="e.g. https://suspicious-bank-login-update.com")
scan_clicked = st.button("🚨 Start Autonomous Forensic Analysis")
st.markdown("</div>", unsafe_allow_html=True)

if scan_clicked:
    if not url_to_scan:
        st.error("Please enter a valid URL.")
    else:
        # Initialize Coordinator
        coordinator = CoordinatorAgent(api_key=api_key_input)
        
        # Terminal-style real-time log area
        st.markdown("### 🖥️ Live Agent Collaboration Stream")
        log_placeholder = st.empty()
        
        # Helper function to refresh live logs
        async def update_logs():
            while True:
                log_html = "<div class='terminal-container'>"
                for line in coordinator.collaboration_logs:
                    # Color coding agents
                    if "[Coordinator]" in line:
                        line = f"<span style='color: #38bdf8;'>{line}</span>"
                    elif "[Scraper Agent]" in line:
                        line = f"<span style='color: #f59e0b;'>{line}</span>"
                    elif "[Code Analyst Agent]" in line:
                        line = f"<span style='color: #a855f7;'>{line}</span>"
                    elif "[Reporter Agent]" in line:
                        line = f"<span style='color: #ec4899;'>{line}</span>"
                    
                    log_html += f"<div class='terminal-line'>{line}</div>"
                log_html += "</div>"
                log_placeholder.markdown(log_html, unsafe_allow_html=True)
                await asyncio.sleep(0.5)

        # Run both log updater and investigator concurrently
        async def run_investigation():
            log_task = asyncio.create_task(update_logs())
            try:
                result = await coordinator.investigate(url_to_scan)
                return result
            finally:
                log_task.cancel()

        with st.spinner("Agents are collaborating on link auditing..."):
            result = asyncio.run(run_investigation())
            
        # Final terminal update to show all logs complete
        log_html = "<div class='terminal-container'>"
        for line in coordinator.collaboration_logs:
            if "[Coordinator]" in line:
                line = f"<span style='color: #38bdf8;'>{line}</span>"
            elif "[Scraper Agent]" in line:
                line = f"<span style='color: #f59e0b;'>{line}</span>"
            elif "[Code Analyst Agent]" in line:
                line = f"<span style='color: #a855f7;'>{line}</span>"
            elif "[Reporter Agent]" in line:
                line = f"<span style='color: #ec4899;'>{line}</span>"
            log_html += f"<div class='terminal-line'>{line}</div>"
        log_html += "</div>"
        log_placeholder.markdown(log_html, unsafe_allow_html=True)

        if result.get("status") == "blocked":
            st.error(result.get("error"))
        elif result.get("status") == "error":
            st.error(f"Scan failed: {result.get('error')}")
        else:
            # Successfully scanned
            scraper_data = result["scraper_data"]
            analyst_data = result["analyst_data"]
            report_data = result["report_data"]
            
            st.success("Investigation complete!")
            
            # --- Forensics Results Dashboard ---
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 📊 Threat Assessment")
                
                # Render Threat Gauge
                score = report_data["final_score"]
                score_class = "score-container"
                if score >= 70:
                    score_class += " score-critical"
                elif score >= 40:
                    score_class += " score-warning"
                    
                st.markdown(f"""
                <div class="{score_class}">
                    <div class="score-num">{score}</div>
                    <div class="score-label">Risk Score</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Verdict:** {report_data['threat_level']}")
                st.markdown(f"**Page Title:** `{scraper_data['title']}`")
                st.markdown(f"**SSL Protocol:** `{'HTTPS' if scraper_data['url'].startswith('https') else 'HTTP'}`")
                
                # Captured Screenshot
                screenshot_path = scraper_data.get("screenshot_path")
                if screenshot_path and os.path.exists(screenshot_path):
                    st.markdown("### 📸 Suspect Snapshot")
                    st.image(screenshot_path, caption="Automated headless capture of target page", use_column_width=True)
                
            with col2:
                st.markdown("### 🕵️‍♂️ Forensics Breakdown")
                
                # Interactive Forensic Tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📝 Forensic Report", 
                    "👁️ Multimodal Visuals", 
                    "💻 Code & Obfuscation Audit",
                    "📦 Scraped Meta Info"
                ])
                
                with tab1:
                    st.markdown(report_data["markdown_report"])
                    # Download button for forensic report
                    st.download_button(
                        label="📥 Download Markdown Forensic Report",
                        data=report_data["markdown_report"],
                        file_name=f"forensic_report_{url_to_scan.replace('/', '_')}.md",
                        mime="text/markdown"
                    )
                    
                with tab2:
                    st.markdown("### Multimodal Visual Audit (Gemini 1.5)")
                    st.write(report_data["visual_findings"])
                    
                with tab3:
                    st.markdown("### Code Analyst Deception Findings")
                    st.markdown(analyst_data["ai_threat_assessment"])
                    
                    st.markdown("---")
                    st.markdown("### Suspicious DOM Indicators")
                    if not analyst_data["indicators"]:
                        st.info("No suspicious elements or obfuscation tags found in raw DOM analysis.")
                    else:
                        for ind in analyst_data["indicators"]:
                            severity_color = "red" if ind["severity"] == "HIGH" else "orange"
                            st.markdown(f"- :**{ind['severity']}** ({ind['type']}): <span style='color: {severity_color};'>{ind['description']}</span>", unsafe_allow_html=True)
                            
                with tab4:
                    st.markdown("### Scraped Forms & Input Targets")
                    forms = scraper_data.get("forms", [])
                    if not forms:
                        st.info("No interactive forms detected on page.")
                    else:
                        for f in forms:
                            st.markdown(f"**Form Action:** `{f['action'] or '/'}` | **Method:** `{f['method'] or 'POST'}`")
                            st.json(f["inputs"])
                            st.markdown("---")
                            
                    st.markdown("### Scraped Script Assets")
                    scripts = scraper_data.get("scripts", [])
                    if not scripts:
                        st.info("No script tags found.")
                    else:
                        for s in scripts[:15]: # Show first 15 scripts
                            st.markdown(f"- Source: `{s['src'] or 'Inline Script'}`")
