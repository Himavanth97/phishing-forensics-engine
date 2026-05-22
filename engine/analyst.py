import re
import google.generativeai as genai

class CodeAnalystAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)

    def analyze_rules(self, scraper_data: dict) -> dict:
        """
        Runs fast, deterministic cybersecurity rules against the scraped HTML/DOM
        to flag suspicious indicators.
        """
        html = scraper_data.get("html", "")
        forms = scraper_data.get("forms", [])
        scripts = scraper_data.get("scripts", [])
        links = scraper_data.get("links", [])
        url = scraper_data.get("url", "")
        
        indicators = []
        threat_score = 0
        
        # 1. Inspect forms for credential harvesting
        for f in forms:
            action = f.get("action") or ""
            inputs = f.get("inputs") or []
            
            # Check action URL
            if action and not action.startswith(('/', 'http://localhost', 'https://localhost')):
                if 'http' in action and not url.split('/')[2] in action:
                    indicators.append({
                        "severity": "HIGH",
                        "type": "credential_harvesting",
                        "description": f"Form action targets an external/unrelated domain: '{action}'"
                    })
                    threat_score += 35
                    
            # Check inputs
            has_password = False
            for inp in inputs:
                inp_type = (inp.get("type") or "").lower()
                inp_name = (inp.get("name") or "").lower()
                
                if inp_type == "password" or "pass" in inp_name:
                    has_password = True
                    
            if has_password:
                indicators.append({
                    "severity": "MEDIUM",
                    "type": "sensitive_input",
                    "description": "Form contains a password input field, high potential for credential harvesting."
                })
                threat_score += 20

        # 2. Check for script obfuscation or suspicious patterns
        suspicious_js_keywords = ['eval(', 'unescape(', 'document.write(', 'String.fromCharCode', 'base64', 'atob(']
        for s in scripts:
            content = s.get("inline_content") or ""
            src = s.get("src") or ""
            
            # Suspicious source domain
            if src and any(domain in src for domain in ['freehost', '000webhost', 'tempmail', 'ngrok', 'localtunnel']):
                indicators.append({
                    "severity": "HIGH",
                    "type": "malicious_script_host",
                    "description": f"Script loaded from a known temporary/free host: '{src}'"
                })
                threat_score += 30
                
            # Obfuscation keywords in inline script
            found_keywords = [kw for kw in suspicious_js_keywords if kw in content]
            if found_keywords:
                indicators.append({
                    "severity": "MEDIUM",
                    "type": "obfuscated_javascript",
                    "description": f"Inline script uses potential obfuscation methods: {', '.join(found_keywords)}"
                })
                threat_score += 15

        # 3. Check domain/brand keyword mismatch (Brand Impersonation)
        famous_brands = ['google', 'microsoft', 'apple', 'paypal', 'netflix', 'amazon', 'facebook', 'instagram', 'bankofamerica', 'chase', 'wellsFargo']
        url_lower = url.lower()
        title_lower = scraper_data.get("title", "").lower()
        
        for brand in famous_brands:
            if brand in title_lower and brand not in url_lower:
                indicators.append({
                    "severity": "HIGH",
                    "type": "brand_impersonation",
                    "description": f"Page title claims to be associated with '{brand.capitalize()}', but the URL domain does not contain it."
                })
                threat_score += 40

        # Cap the threat score at 100 for rule-based
        threat_score = min(threat_score, 100)
        
        return {
            "rule_threat_score": threat_score,
            "indicators": indicators
        }

    async def analyze_with_ai(self, scraper_data: dict, rule_findings: dict) -> dict:
        """
        Uses the Gemini model to analyze the full context (HTML structure, suspicious scripts,
        and rule findings) and provide a professional, deep cybersecurity audit.
        """
        if not self.api_key:
            return {
                "ai_threat_assessment": "Gemini API Key missing. Skipping AI deep code analysis.",
                "ai_score_adjustment": 0,
                "phishing_indicators": []
            }

        try:
            # We construct a optimized prompt containing the HTML skeleton and findings
            html_snippet = scraper_data.get("html", "")[:4000] # Cap HTML size to fit model context efficiently
            forms = scraper_data.get("forms", [])
            indicators = rule_findings.get("indicators", [])

            prompt = f"""
You are a Lead Cybersecurity Analyst and Forensics Expert investigating a potential phishing link.

We scanned this URL: {scraper_data.get('url')}
Page Title: {scraper_data.get('title')}

Here is the parsed Form Structures:
{forms}

Here is a snippet of the page HTML DOM:
```html
{html_snippet}
```

The rule-based analysis flagged these potential threats:
{indicators}

Please perform an in-depth security analysis on this code:
1. Examine if this page uses brand impersonation or deceptive layouts.
2. Determine if the form actions are designed to harvest credentials or direct tokens to malicious handlers.
3. Identify any obfuscated scripts or redirection techniques.
4. Calculate an AI Threat Confidence score (0 to 100, where 100 is definitely phishing).

Format your response in structured Markdown with headings:
- **Deception & Brand Impersonation**: Describe any visual or textual spoofing.
- **Form & Input Security**: Detail any credential harvesting signals.
- **Malicious & Obfuscated Code**: Analyze inline or loaded scripts.
- **AI Threat Confidence Score**: [Score from 0 to 100]
"""
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = await asyncio.to_thread(model.generate_content, prompt)
            
            ai_text = response.text
            
            # Extract score from response using regex
            score_match = re.search(r'AI Threat Confidence Score:\s*(\d+)', ai_text, re.IGNORECASE)
            ai_score = int(score_match.group(1)) if score_match else rule_findings["rule_threat_score"]
            
            return {
                "ai_threat_assessment": ai_text,
                "ai_threat_score": ai_score
            }
        except Exception as e:
            return {
                "ai_threat_assessment": f"Error running AI analysis: {str(e)}",
                "ai_threat_score": rule_findings["rule_threat_score"]
            }
            
    async def run(self, scraper_data: dict) -> dict:
        """
        Runs both rules and AI deep analysis, then merges findings.
        """
        rule_findings = self.analyze_rules(scraper_data)
        ai_findings = await self.analyze_with_ai(scraper_data, rule_findings)
        
        return {
            "rule_threat_score": rule_findings["rule_threat_score"],
            "indicators": rule_findings["indicators"],
            "ai_threat_assessment": ai_findings.get("ai_threat_assessment", ""),
            "ai_threat_score": ai_findings.get("ai_threat_score", rule_findings["rule_threat_score"])
        }
