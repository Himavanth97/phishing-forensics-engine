import asyncio
import os
from engine.coordinator import CoordinatorAgent
from utils.safety import normalize_url, is_safe_to_scan

async def main():
    print("==================================================")
    print("🛡️  PHISHING FORENSICS ENGINE - AUTOMATED TESTING")
    print("==================================================")

    # 1. Test safety utility
    print("\n[Test 1] Testing safety checks...")
    urls = [
        ("google.com", "https://google.com", True),
        ("http://127.0.0.1:8000", "http://127.0.0.1:8000", False),
        ("localhost", "https://localhost", False),
        ("https://wikipedia.org", "https://wikipedia.org", True)
    ]
    
    for input_url, expected_norm, expected_safe in urls:
        norm = normalize_url(input_url)
        safe = is_safe_to_scan(norm)
        print(f"  Input: {input_url} -> Normalized: {norm} -> Safe: {safe}")
        assert safe == expected_safe, f"Safety check failed for {input_url}"
    print("✅ Safety checks passed.")

    # 2. Test coordination and scraping
    print("\n[Test 2] Testing scraper & coordinator (Wikipedia)...")
    coordinator = CoordinatorAgent(api_key=None)
    
    # Scan wikipedia.org
    target = "https://wikipedia.org"
    result = await coordinator.investigate(target)
    
    print(f"  Scan Status: {result.get('status')}")
    if result.get("status") == "completed":
        scraper = result["scraper_data"]
        analyst = result["analyst_data"]
        report = result["report_data"]
        
        print(f"  Page Title: {scraper.get('title')}")
        print(f"  Screenshot Path: {scraper.get('screenshot_path')}")
        print(f"  Rule Threat Score: {analyst.get('rule_threat_score')}/100")
        print(f"  Final Score: {report.get('final_score')}/100")
        print(f"  Verdicts Level: {report.get('threat_level')}")
        
        assert scraper.get("title") is not None, "Title scraping failed"
        assert scraper.get("screenshot_path") != "", "Screenshot generation failed"
        assert os.path.exists(scraper.get("screenshot_path")), "Screenshot file not found on disk"
        print("✅ Scraper and Coordinator test passed successfully!")
    else:
        print(f"❌ Scan failed: {result.get('error')}")
        exit(1)

    print("\n==================================================")
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
