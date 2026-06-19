"""
DeepThought Assignment — Research Automation Scripts
Part A: Utility functions used during company research
Part B: Prototype scoring pipeline (scale-up demonstration)

These scripts demonstrate the approach described in the methodology and
1000-company proposal. Not all are fully production-ready — they illustrate
the logic and tech stack that would be used at scale.
"""

import csv
import json
import time
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. HARD PRE-FILTER
#    Input: raw universe CSV with company names
#    Output: filtered list (removes traders, no-website, etc.)
# ---------------------------------------------------------------------------

TRADER_KEYWORDS = [
    "trading", "traders", "imports", "importers", "exports", "exporters",
    "distributors", "distribution", "enterprises", "agencies", "solutions pvt"
]

def hard_prefilter(companies: list[dict]) -> list[dict]:
    """
    Applies deterministic pre-filter rules before any AI scoring.
    Returns only companies that pass all pre-filter gates.
    """
    passed = []
    failed = []

    for company in companies:
        name = company.get("company_name", "").lower()
        website = company.get("website", "").strip()
        revenue = company.get("revenue_band", "")

        # Gate 1: No website
        if not website or website in ["", "N/A", "not found"]:
            company["fail_reason"] = "No website found"
            failed.append(company)
            continue

        # Gate 2: Trader/distributor keywords in name
        if any(kw in name for kw in TRADER_KEYWORDS):
            company["fail_reason"] = f"Trader/distributor keyword in name: '{name}'"
            failed.append(company)
            continue

        # Gate 3: Revenue known to be above ceiling
        if revenue == ">Rs.500Cr":
            company["fail_reason"] = "Revenue above Rs.500Cr ceiling"
            failed.append(company)
            continue

        passed.append(company)

    print(f"Pre-filter: {len(passed)} passed, {len(failed)} failed out of {len(companies)}")
    return passed, failed


# ---------------------------------------------------------------------------
# 2. WEBSITE SCRAPER (prototype)
#    Demonstrates the scraping logic for the 1000-company pipeline
# ---------------------------------------------------------------------------

TARGET_PATHS = [
    "/", "/about", "/about-us", "/company", "/who-we-are",
    "/leadership", "/team", "/management", "/board",
    "/products", "/services", "/capabilities", "/what-we-make",
    "/news", "/media", "/press", "/blog", "/updates",
    "/careers", "/jobs", "/join-us",
    "/certifications", "/quality", "/compliance"
]

MAX_TOKENS_PER_COMPANY = 8000  # ~6,000 words

def scrape_company(url: str) -> str:
    """
    Scrapes a company website and returns concatenated text.
    In production, this uses Playwright for JS-rendered sites.
    This is a simplified version using requests for demonstration.
    """
    try:
        import requests
        from bs4 import BeautifulSoup

        base_url = url.rstrip("/")
        all_text = []

        for path in TARGET_PATHS:
            try:
                response = requests.get(
                    f"{base_url}{path}",
                    headers={"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"},
                    timeout=10
                )
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Remove script and style tags
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text(separator=" ", strip=True)
                    all_text.append(f"[PAGE: {path}]\n{text}")

                time.sleep(1.5)  # Polite delay between requests

            except Exception:
                continue  # Skip unavailable pages

        combined = "\n\n".join(all_text)
        # Truncate to token limit (rough: 1 token ~ 4 chars)
        return combined[:MAX_TOKENS_PER_COMPANY * 4]

    except ImportError:
        return "[Scraping libraries not installed — install requests and beautifulsoup4]"


# ---------------------------------------------------------------------------
# 3. AI SCORING PROMPT
#    The prompt sent to Claude Haiku for first-pass ICP scoring
# ---------------------------------------------------------------------------

HAIKU_SCORING_PROMPT = """
You are an ICP analyst for DeepThought, a B2B consulting company.
Your task: evaluate whether a company matches the Federer ICP.

A Federer company is:
- A real manufacturer (not a trader, distributor, CRO, or testing lab)
- India-headquartered with primary operations in India
- Founder/MD has technical background (PhD, IIT/NIT, scientist) OR has built operational systems (ERP, SAP, structured costing)
- Operating in a sector with growth tailwinds (PLI, China+1, Make-in-India, export demand)
- Showing active growth signals in last 18 months (hiring, new facility, new certifications, revenue growth)
- Has evidence of structured digital/operational systems (ERP, SAP, ISO quality systems, MIS dashboards)
- Shows leadership depth beyond sole founder (gen-2 on board, professional managers hired, multiple portfolios)

Scoring rubric:
- Weak = 0 points
- Moderate = half the criterion weight
- Strong = full criterion weight
Weights: C3=20, C4=15, C5=15, C6=15, C7=20, C8=15

IMPORTANT:
- ISO 9001 alone does NOT count as differentiation (C3). It must be + DSIR/USFDA/patents/proprietary products.
- C6 growth signals must be from last 18 months. Ignore press articles older than Jan 2023.
- If the company sells "solutions" or "services" but mentions manufacturing facility/plant, score E1 as PASS.
- Score only what's evidenced in the text. Don't infer beyond the evidence.

Return ONLY a valid JSON object. No preamble, no markdown, no explanation outside the JSON.

{
  "company_name": "...",
  "E1_producer": "PASS or FAIL",
  "E1_evidence": "one sentence",
  "E2_accessible": "PASS or FAIL",
  "E2_evidence": "one sentence",
  "C3_score": "Weak or Moderate or Strong",
  "C3_evidence": "one sentence",
  "C4_score": "Weak or Moderate or Strong",
  "C4_evidence": "one sentence",
  "C5_score": "Weak or Moderate or Strong",
  "C5_evidence": "one sentence",
  "C6_score": "Weak or Moderate or Strong",
  "C6_evidence": "one sentence",
  "C7_score": "Weak or Moderate or Strong",
  "C7_evidence": "one sentence",
  "C8_score": "Weak or Moderate or Strong",
  "C8_evidence": "one sentence",
  "total_score": <number 0-100>,
  "band": "A or B or C or D",
  "verdict": "Strong Pass or Pass or Borderline or Fail",
  "confidence": "High or Medium or Low",
  "confidence_flags": ["list criteria where evidence was thin or ambiguous"]
}
"""


# ---------------------------------------------------------------------------
# 4. AI SCORING CALL (prototype — uses Anthropic API)
# ---------------------------------------------------------------------------

def score_company_with_ai(company_text: str, company_name: str) -> dict:
    """
    Calls Claude Haiku to score a company's website text against the Federer ICP.
    Returns a parsed JSON result dict.
    
    In production: use async batch processing for parallel calls.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"{HAIKU_SCORING_PROMPT}\n\n[COMPANY: {company_name}]\n\n[WEBSITE TEXT]:\n{company_text}"
                }
            ]
        )

        response_text = message.content[0].text.strip()
        # Clean potential markdown fences
        response_text = re.sub(r"```json|```", "", response_text).strip()
        return json.loads(response_text)

    except ImportError:
        return {"error": "anthropic library not installed — pip install anthropic"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "raw": response_text}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# 5. AUTO-QA FLAGS
#    Runs after AI scoring to flag low-confidence or likely-wrong scores
# ---------------------------------------------------------------------------

def run_auto_qa_flags(scored_companies: list[dict]) -> list[dict]:
    """
    Applies programmatic QA rules to scored companies.
    Returns the list with a 'qa_flag' field added where relevant.
    """
    flagged = []

    for company in scored_companies:
        flags = []

        # Flag 1: C3 evidence mentions only ISO 9001 without other differentiators
        c3_evidence = company.get("C3_evidence", "").lower()
        if company.get("C3_score") == "Moderate" and "iso 9001" in c3_evidence:
            if not any(term in c3_evidence for term in ["dsir", "patent", "usfda", "eu-gmp", "proprietary", "specialized"]):
                flags.append("C3_possible_inflation: ISO 9001 alone used as differentiation evidence")

        # Flag 2: C6 evidence references old dates
        c6_evidence = company.get("C6_evidence", "")
        old_years = re.findall(r"\b(2018|2019|2020|2021|2022)\b", c6_evidence)
        if old_years and company.get("C6_score") in ["Moderate", "Strong"]:
            flags.append(f"C6_stale_evidence: references year(s) {old_years} — may not meet 18-month recency requirement")

        # Flag 3: Low confidence flagged by AI
        if company.get("confidence") == "Low":
            flags.append("AI_low_confidence: model flagged low confidence on this company")

        # Flag 4: Suspiciously perfect score (100/100)
        if company.get("total_score") == 100:
            flags.append("Perfect_score_check: verify all 6 criteria evidence manually")

        # Flag 5: E1 FAIL but website mentions facility
        if company.get("E1_producer") == "FAIL":
            website_text = company.get("_scraped_text", "").lower()
            if any(term in website_text for term in ["manufacturing plant", "production facility", "our plant", "factory"]):
                flags.append("E1_possible_false_negative: FAIL scored but website mentions manufacturing facility")

        if flags:
            company["qa_flags"] = flags
            flagged.append(company)
        else:
            company["qa_flags"] = []

    print(f"Auto-QA: {len(flagged)} companies flagged out of {len(scored_companies)}")
    return scored_companies, flagged


# ---------------------------------------------------------------------------
# 6. SCORE CALCULATOR
#    Converts Weak/Moderate/Strong to numeric scores
# ---------------------------------------------------------------------------

WEIGHTS = {"C3": 20, "C4": 15, "C5": 15, "C6": 15, "C7": 20, "C8": 15}

def calculate_total_score(result: dict) -> int:
    """Recalculates total score from individual criterion scores."""
    total = 0
    for criterion, weight in WEIGHTS.items():
        score_key = f"{criterion}_score"
        score = result.get(score_key, "Weak")
        if score == "Strong":
            total += weight
        elif score == "Moderate":
            total += weight // 2
    return total

def get_band(score: int) -> str:
    if score >= 80:
        return "A — Strong Federer"
    elif score >= 60:
        return "B — Probable Federer"
    elif score >= 40:
        return "C — Borderline"
    else:
        return "D — Not ICP"


# ---------------------------------------------------------------------------
# 7. CSV EXPORT
#    Writes final scored companies to CSV in the assignment format
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "company_name", "website", "city", "segment",
    "E1_producer", "E1_evidence", "E2_accessible", "E2_evidence",
    "C3_score", "C3_evidence", "C4_score", "C4_evidence",
    "C5_score", "C5_evidence", "C6_score", "C6_evidence",
    "C7_score", "C7_evidence", "C8_score", "C8_evidence",
    "total_score", "band", "verdict", "confidence", "qa_flags"
]

def export_to_csv(companies: list[dict], output_path: str):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for company in companies:
            # Convert qa_flags list to string for CSV
            if isinstance(company.get("qa_flags"), list):
                company["qa_flags"] = " | ".join(company["qa_flags"])
            writer.writerow(company)
    print(f"Exported {len(companies)} companies to {output_path}")


# ---------------------------------------------------------------------------
# DEMONSTRATION: Run pipeline on a small test set
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("DeepThought Assignment — Research Pipeline Demo")
    print("=" * 50)

    # Example: demonstrate score calculator on sample data
    sample_result = {
        "company_name": "Example Specialty Chemicals Pvt Ltd",
        "C3_score": "Strong",
        "C4_score": "Strong",
        "C5_score": "Strong",
        "C6_score": "Moderate",
        "C7_score": "Strong",
        "C8_score": "Moderate",
    }

    score = calculate_total_score(sample_result)
    band = get_band(score)
    print(f"\nSample company score: {score}/100 — {band}")

    # Show what the pre-filter would do
    test_companies = [
        {"company_name": "ABC Trading Pvt Ltd", "website": "abc.com", "revenue_band": "Rs.30-100Cr"},
        {"company_name": "XYZ Chemicals Pvt Ltd", "website": "xyz.com", "revenue_band": "Rs.100-300Cr"},
        {"company_name": "No Website Corp", "website": "", "revenue_band": "Rs.30-100Cr"},
        {"company_name": "Large Corp Ltd", "website": "largecorp.com", "revenue_band": ">Rs.500Cr"},
    ]

    passed, failed = hard_prefilter(test_companies)
    print(f"\nPre-filter demo:")
    print(f"  Passed: {[c['company_name'] for c in passed]}")
    print(f"  Failed: [{c['company_name']}: {c['fail_reason']} for c in failed]}")

    print("\nPipeline functions ready. Full run requires:")
    print("  pip install anthropic requests beautifulsoup4 playwright")
    print("  playwright install chromium")
