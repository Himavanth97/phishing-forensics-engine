# 🛡️ Autonomous Multi-Agent Phishing Forensics Engine

An autonomous, collaborative cybersecurity forensic system that uses specialized AI agents to investigate suspicious links, extract DOM assets, capture full-page snapshots, analyze code for obfuscation/deception, and synthesize unified multi-page threat reports.

Developed to prove role-based multi-agent orchestration, headless browser sandboxing, and multimodal visual threat detection in cybersecurity.

---

## 🤖 Multi-Agent Collaboration Roster

1. **🕵️‍♂️ Coordinator Agent:** Manages execution state transitions, enforces SSRF network boundaries, and streams real-time coordination logging.
2. **🌐 Scraper Agent:** Safely navigates the URL inside a sandboxed headless Playwright browser, retrieves raw HTML/DOM source, captures high-resolution visual screenshots, and logs form elements.
3. **💻 Code Analyst Agent:** Audits Javascript/HTML structures for obfuscation (e.g. `eval`, hex encryption) and detects brand spoofing/credential-harvesting fields.
4. **🎨 Reporter Agent:** Performs visual identity analysis of screenshots using Gemini 1.5 Multimodal API and synthesizes a structured Markdown forensics report with a weighted Threat Score (0-100).

---

## 🛠️ Technology Stack
- **Orchestration:** Lightweight Python-based state-machine coordinator.
- **Headless Browser:** Playwright (Python).
- **Multimodal AI / LLM:** Gemini 1.5 Pro / Flash.
- **User Interface:** Streamlit (Custom premium cyber dark-mode interface with glassmorphic cards and a retro glowing terminal logs stream).

---

## 🚀 Installation & Running

### 1. Pre-requisites
Make sure you have Python 3.8+ installed.

### 2. Setup Virtual Environment & Dependencies
```bash
# Clone the repository and navigate inside
cd phishing-forensics-engine

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Playwright browser dependencies
playwright install chromium
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(You can also input your Gemini API Key directly in the Streamlit Sidebar at runtime).*

### 4. Start the Engine Dashboard
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser to start scanning suspect URLs!

---

## 🧪 Running Automated Verification Tests
We have built an automated test suite to verify the safety checks, DOM scraping, and screenshot generation capabilities out-of-the-box:
```bash
python3 verify.py
```

---

## 📁 Repository Structure
```
phishing-forensics-engine/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app.py              # Streamlit Dashboard UI
├── verify.py           # Automated Test Suite
├── engine/
│   ├── __init__.py
│   ├── coordinator.py  # Orchestrates agents & collaboration logs
│   ├── scraper.py      # Playwright browser automation & asset scraping
│   ├── analyst.py      # Static and semantic source code check
│   └── reporter.py     # Multimodal visual analysis & report compiler
└── utils/
    ├── __init__.py
    └── safety.py       # SSRF prevention & URL normalization
```
