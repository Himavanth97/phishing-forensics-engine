# Contributing to Phishing Forensics Engine

Thank you for choosing to contribute to the Phishing Forensics Engine! Please follow the steps below to set up your environment, write clean code, and run tests.

---

## 1. Local Development Setup

To run this project locally, you will need **Python 3.9+** and a **Google Gemini API Key** (for cognitive vision features).

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Himavanth97/phishing-forensics-engine.git
   cd phishing-forensics-engine
   ```

2. **Initialize a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**:
   This step is absolutely critical. Playwright requires dynamic browser binaries to render and capture target sites:
   ```bash
   playwright install chromium
   ```

5. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and input your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

6. **Run the Dashboard**:
   Launch the Streamlit interactive dashboard:
   ```bash
   streamlit run app.py
   ```

---

## 2. Testing & Verification

To verify that your installation is correctly configured, browsers are installed, and credentials are valid, run our diagnostics script:
```bash
python3 verify.py
```
Ensure all system tests return a passing status before making edits.

---

## 3. Code Standards & Architecture

* **Type Hinting**: Always use type hints in your function definitions (e.g. `def analyze_url(url: str) -> Dict[str, Any]:`).
* **Security Mindset**: Since this tool interacts with unverified, potentially malicious URLs, **never** execute raw HTML content or scripts inside the analyst's client. Keep browsers headless and restrict file accesses.
* **Linting & Formatting**: Follow PEP 8 guidelines. Run standard formatters such as `black` or `flake8` if desired.
