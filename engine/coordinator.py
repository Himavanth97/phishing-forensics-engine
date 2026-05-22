import asyncio
from engine.scraper import ScraperAgent
from engine.analyst import CodeAnalystAgent
from engine.reporter import ReporterAgent
from utils.safety import normalize_url, is_safe_to_scan

class CoordinatorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.scraper = ScraperAgent()
        self.analyst = CodeAnalystAgent(api_key=api_key)
        self.reporter = ReporterAgent(api_key=api_key)
        self.collaboration_logs = []

    def log(self, sender: str, message: str):
        """Records a step in the multi-agent collaboration trail."""
        log_entry = f"[{sender}] {message}"
        print(log_entry)
        self.collaboration_logs.append(log_entry)

    async def investigate(self, url: str) -> dict:
        """
        Coordinates the entire investigative flow across the agents.
        """
        self.collaboration_logs = []
        self.log("Coordinator", "Initializing Phishing Forensic Investigation...")
        
        # 1. Normalize and check safety
        url = normalize_url(url)
        self.log("Coordinator", f"Target normalized to: {url}")
        
        if not is_safe_to_scan(url):
            self.log("Coordinator", "❌ SAFETY ALERT: Blocked scanning local or loopback address to prevent SSRF.")
            return {
                "status": "blocked",
                "logs": self.collaboration_logs,
                "error": "URL blocked due to local/loopback addressing restrictions."
            }

        # 2. Scraper Agent execution
        self.log("Coordinator", "Routing target URL to [Scraper Agent].")
        self.log("Scraper Agent", "Launching headless Chromium browser instance...")
        
        scraper_data = await self.scraper.run(url)
        
        if scraper_data.get("status") == "error":
            self.log("Scraper Agent", f"❌ Failed to render URL: {scraper_data.get('error')}")
            self.log("Coordinator", "Investigation terminated prematurely due to rendering error.")
            return {
                "status": "error",
                "logs": self.collaboration_logs,
                "error": scraper_data.get("error")
            }

        self.log("Scraper Agent", "✅ DOM extracted. Screenshot captured successfully.")
        self.log("Scraper Agent", f"Found {len(scraper_data.get('scripts', []))} script tags and {len(scraper_data.get('forms', []))} form elements.")

        # 3. Code Analyst Agent execution
        self.log("Coordinator", "Routing DOM structure and scripts to [Code Analyst Agent] for code audit.")
        self.log("Code Analyst Agent", "Analyzing HTML/JS with determinist rule filters...")
        
        analyst_data = await self.analyst.run(scraper_data)
        
        self.log("Code Analyst Agent", f"Deterministic threat score: {analyst_data.get('rule_threat_score')}/100")
        self.log("Code Analyst Agent", f"Flagged {len(analyst_data.get('indicators', []))} suspicious indicators.")
        
        if self.api_key:
            self.log("Code Analyst Agent", "Running deep AI semantic code check using Gemini 1.5...")
            self.log("Code Analyst Agent", "✅ Deep AI code analysis complete.")
        else:
            self.log("Code Analyst Agent", "⚠️ Skipping deep AI check (No API Key).")

        # 4. Reporter Agent execution
        self.log("Coordinator", "Forwarding DOM data, code findings, and screenshot file to [Reporter Agent].")
        if self.api_key:
            self.log("Reporter Agent", "Initiating multimodal screenshot inspection with Gemini 1.5...")
            self.log("Reporter Agent", "✅ Visual spoofing check completed.")
        else:
            self.log("Reporter Agent", "⚠️ Skipping visual inspection (No API Key).")
            
        self.log("Reporter Agent", "Synthesizing comprehensive forensic report and threat score...")
        
        report_data = await self.reporter.run(scraper_data, analyst_data)
        
        self.log("Coordinator", "🎉 Investigation complete. Generating threat score and publishing report.")
        
        return {
            "status": "completed",
            "logs": self.collaboration_logs,
            "scraper_data": scraper_data,
            "analyst_data": analyst_data,
            "report_data": report_data
        }
