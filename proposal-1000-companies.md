# Proposal: 1000 ICP-Qualified Companies in One Month
### DeepThought Business Analytics Internship — Part B, Question 2
**Utkarsh Gupta**

---

## Goal

Build a verified list of 1000 companies that match DeepThought's Federer ICP — Indian specialty manufacturers, Rs.50Cr–Rs.500Cr revenue, promoter-driven, differentiated product, technical decision-maker, active growth signals — within 30 calendar days.

---

## The Core Logic

From Part A: the yield rate on investigated companies is ~30%. To get 1000 qualified passes, I need to investigate ~3,300–3,500 companies. The plan works backward from this number.

The constraint isn't sourcing — India has tens of thousands of manufacturers. The constraint is **qualification quality at speed**. A bulk scrape of company names is worthless. Every company in the final list needs evidence on all 6 criteria.

The pipeline therefore has three phases:
1. **Source** — build the raw universe fast (week 1)
2. **Score** — run automated ICP scoring via AI (weeks 2–3)
3. **Verify** — human QA on borderline and low-confidence cases (weeks 3–4)

---

## The Funnel

```
Raw Universe (3,300–3,500 companies)
    ↓ Hard pre-filters (auto-disqualify rules, no AI needed)
Screened Pool (~2,200–2,500 companies)
    ↓ AI-assisted ICP scoring (Claude Haiku, parallel)
First-Pass Qualified (~1,100–1,300 companies)
    ↓ Human QA on flagged + borderline
Final Verified List (1,000 companies)
```

---

## Week 1: Build the Universe

Target: 3,300–3,500 unique companies with at minimum name, city, website, rough segment tag.

### Source 1 — DSIR-Recognized R&D Units (dsir.gov.in)
**What:** Public list of companies with government-recognized in-house R&D units. ~3,000+ companies nationally.  
**Why it works:** DSIR recognition directly pre-filters for C3 (differentiation — R&D investment) and C4 (technical decision-maker — someone built and maintains a recognized R&D unit). It's a structural signal that the company thinks technically.  
**How:** Download the DSIR list PDF from dsir.gov.in. Parse to extract company name, city, industry. Filter to manufacturing in target segments (chemicals, pharma, agri-inputs, medical devices, electronics, engineering).  
**Expected yield:** ~800–1,000 companies after segment and city filtering.  
**Limitation:** Skews toward established companies. Misses startups that haven't applied for DSIR yet.

### Source 2 — Trade Expo Exhibitor Directories
**What:** Industry expos publish exhibitor lists. Targets: CPhI India (pharma/chem), BioAsia (biotech), Aero India (defence), ELECRAMA (electronics/electrical), IMTEX (machine tools), Agri Intex (agri-inputs), PackEx India (industrial packaging), Lab India (lab instruments).  
**Why it works:** Paying Rs.2–10L for an expo booth is a growth signal (C6) — stagnant companies don't exhibit. Expo segments map directly to our ICP baskets.  
**How:** Most expos publish exhibitor directories online. Some require registration (free). Build a Playwright scraper to extract exhibitor name + website + product category.  
**Expected yield:** ~600–800 companies across 8 expos, after deduplication.  
**Limitation:** Biased toward companies with marketing budgets. May miss bootstrapped Rs.50Cr manufacturers.

### Source 3 — BSE SME + NSE Emerge Listed Companies
**What:** Small-cap listed companies in manufacturing sectors.  
**Why it works:** Public financials immediately answer C6 (growth — revenue trend visible) and the revenue band question. Annual reports contain leadership bios for C4. Shareholding data confirms C1 (promoter-driven, PE check).  
**How:** Download company master data from BSE SME/NSE Emerge. Filter by: Industry = chemicals/pharma/engineering/medical devices/agri/electronics, Revenue Rs.30Cr–Rs.500Cr.  
**Expected yield:** ~400–500 companies.  
**Limitation:** Only listed companies. Private MSMEs (majority of ICP) don't appear.

### Source 4 — USFDA / EU-GMP / CDSCO Approved Facility Lists
**What:** Regulatory approval lists for pharma and medical device manufacturers.  
**Why it works:** International regulatory approval directly evidences C1 (manufacturer — you can't get USFDA approval without a facility), C3 (differentiation — commodity manufacturers don't pursue international approvals), and C5 (export markets = tailwind).  
**How:** USFDA facility list is searchable at fda.gov/inspections-compliance-enforcement. Filter to India, then to MSME-segment companies (exclude Sun, Cipla, Dr. Reddy's tier). Cross-reference with EU-GMP and CDSCO lists.  
**Expected yield:** ~350–450 companies, filtering out large pharma.  
**Limitation:** Heavy pharma/chem bias. Doesn't cover defence, agri, medtech instrumentation well.

### Source 5 — Industry Association Member Directories
**What:** IDMA (pharma), BDMA (bulk drugs), ACMA (auto components), ELCINA (electronics), FSSAI-registered specialty food producers, SIAM small manufacturers, Seed Association of India, CII members (MSME chapter).  
**Why it works:** Active association membership signals an operating, engaged company. Directories often include segment, product line, and contact information.  
**How:** Most associations publish partial directories publicly; some require registration. Scrape or extract manually. CII state chapter directories are particularly useful.  
**Expected yield:** ~500–600 companies, significant overlap expected.  
**Limitation:** Overlaps heavily with DSIR and expo sources. Deduplication is critical.

### Source 6 — MCA Data via Antigravity / Tofler
**What:** Ministry of Corporate Affairs has all registered Indian companies — NIC codes (industry classification), director details, paid-up capital, registered address.  
**Why it works:** NIC codes allow segment-specific filtering at scale. Director names give DM info for C4 enrichment. Paid-up capital is a size proxy for pre-filtering.  
**How:** Use Antigravity (or Tofler API) to query: NIC codes matching target segments (chemicals: 201xx, 202xx; pharma: 2100; medical devices: 3250; electronics: 261xx; instruments: 265xx) + city + capital range.  
**Expected yield:** ~1,000–1,500 raw records; expect 60% to be dormant, tiny, or wrong-coded.  
**Limitation:** Very noisy. NIC codes are self-reported and frequently incorrect. Requires heavy filtering. No website data in MCA — needs enrichment.

### Source 7 — MIDC / GIDC / TSIIC Industrial Estate Directories
**What:** State industrial development corporations (MIDC Maharashtra, GIDC Gujarat, TSIIC Telangana) publish estate-level company lists for their industrial zones.  
**Why it works:** Companies in named industrial estates are confirmed manufacturers (you lease an MIDC plot to manufacture, not to trade). This pre-filters E1 (manufacturer) without needing AI.  
**How:** MIDC has a company directory on midc.in filterable by estate and industry. GIDC similarly on gidc.gujarat.gov.in.  
**Expected yield:** ~300–400 companies after filtering to target segment estates (e.g., Tarapur MIDC for chemicals, Andheri MIDC for electronics).  
**Limitation:** Covers only estate-based manufacturers. Companies in private industrial parks or self-owned facilities won't appear.

### Week 1 Output
After deduplication across all 7 sources: **3,300–3,500 unique companies** with name, city, segment tag. ~60% will have website URLs. The remaining 40% need website discovery via automated Google search: `"{company name}" "{city}" site:.com OR site:.in`.

| Day | Task |
|-----|------|
| 1–2 | Download and parse DSIR list, BSE/NSE SME data, USFDA facility list. Structured data — fastest to process. |
| 2–3 | Scraper for 8 expo exhibitor directories (Python + Playwright). |
| 3–4 | Extract MIDC/GIDC directories, industry association lists, MCA data via Antigravity. |
| 4–5 | Website discovery for companies without URLs (Google search automation script). |
| 5–6 | Deduplication across all sources. Fuzzy name matching (Levenshtein + CIN number for listed companies). |
| 6–7 | Hard pre-filter: remove names with "Trading" / "Imports" / "Distributors", revenue > Rs.500Cr (if known), no website after discovery attempts. |

---

## Weeks 2–3: Automated ICP Scoring

### The Scraper
For each company with a website, scrape these pages:
- Homepage
- /about, /about-us, /company
- /leadership, /team, /management, /board
- /products, /services, /capabilities
- /news, /media, /press-releases, /blog
- /careers, /jobs
- /certifications, /quality, /compliance

Concatenate scraped text to ~8,000 tokens per company (truncate if longer). Use Playwright (handles JavaScript-rendered sites) with 12-second timeout per page. Respect robots.txt. Rotate user-agents.

**Tech stack:** Python + Playwright for scraping, Claude Haiku for first-pass scoring, Claude Sonnet for borderline re-scoring. PostgreSQL or Google Sheets as master data store.

### The AI Scoring Prompt

System prompt to Claude Haiku (simplified):

```
You are an ICP analyst for a B2B consulting company called DeepThought. 
Your task is to evaluate whether a company matches DeepThought's ideal customer profile (ICP) — the "Federer company."

A Federer company:
- Produces a differentiated product in-house (not a trader, distributor, or generic producer)
- Is India-headquartered with primary operations in India
- Has a technical or systems-thinking founder/MD
- Operates in a growing sector
- Shows active growth signals (hiring, new facility, new certifications, revenue growth, active website)
- Has evidence of structured systems (ERP, quality management, MIS)
- Shows leadership depth beyond solo founder

You will receive the scraped website text of a company. Return ONLY a JSON object with this structure:
{
  "E1_producer": "PASS/FAIL",
  "E1_evidence": "one line",
  "E2_accessible": "PASS/FAIL", 
  "E2_evidence": "one line",
  "C3_score": "Weak/Moderate/Strong",
  "C3_evidence": "one line",
  "C4_score": "Weak/Moderate/Strong",
  "C4_evidence": "one line",
  "C5_score": "Weak/Moderate/Strong",
  "C5_evidence": "one line",
  "C6_score": "Weak/Moderate/Strong",
  "C6_evidence": "one line",
  "C7_score": "Weak/Moderate/Strong",
  "C7_evidence": "one line",
  "C8_score": "Weak/Moderate/Strong",
  "C8_evidence": "one line",
  "total_score": number,
  "band": "A/B/C/D",
  "verdict": "Strong Pass/Pass/Borderline/Fail",
  "confidence": "High/Medium/Low",
  "confidence_flags": ["list any criteria where you had low confidence"]
}
```

### Scoring Pipeline Logic

```python
for company in universe:
    # Step 1: Scrape
    text = scrape_company_website(company.url)
    
    # Step 2: Hard pre-filter before AI call
    if is_trader(company.name) or no_website(company):
        mark_fail("auto-disqualify")
        continue
    
    # Step 3: Haiku first pass
    result = claude_haiku(text, scoring_prompt)
    
    # Step 4: Flag for human QA if:
    if result.verdict == "Borderline" or result.confidence == "Low":
        flag_for_human_qa(company, result)
    
    # Step 5: Sonnet re-score for borderline
    if result.total_score in range(40, 55):
        result = claude_sonnet(text, scoring_prompt)
    
    # Step 6: Store
    save_to_master(company, result)
```

**Cost estimate:**
- Haiku first pass: ~$0.005/company × 2,500 = $12.50 (~Rs.1,050)
- Sonnet re-score on ~20% borderline: ~$0.04/company × 500 = $20 (~Rs.1,680)
- Scraping compute: negligible (local machine or small cloud VM)
- **Total AI cost: ~Rs.2,750** — well within a standard API budget

**Speed estimate:**
- Scraping: ~30 seconds/company with politeness delays, 4 parallel workers = ~5 hours for 2,500 companies
- Haiku scoring: ~3 seconds/company = ~2 hours
- Sonnet re-scoring: ~5 seconds/500 companies = ~45 minutes
- **Total compute: ~8 hours**, spread over 2 days

| Day | Task |
|-----|------|
| 8–9 | Build and test scraper on 50 companies. Debug edge cases (JS-heavy sites, redirect loops, paywalls). |
| 10 | Build scoring pipeline. Test on 15 calibration companies (known passes and fails from Part A). Tune Haiku prompt if accuracy < 80% on calibration set. |
| 11–14 | Run scraper on full 2,500-company screened pool (4 parallel workers). |
| 14–16 | Run Haiku scoring on all scraped companies. |
| 16–17 | Run Sonnet re-scoring on borderline band (total score 40–55). |
| 18 | Compile first-pass results. Expected: ~1,100–1,300 passes, ~400–500 borderline/low-confidence flagged for QA. |

---

## Weeks 3–4: Human QA + Final Assembly

### Why AI Scoring Alone Isn't Enough

From Part A research, I found 4 systematic failure modes in AI scoring:

1. **C3 inflation:** LLM reads "ISO 9001" on the website and scores C3 (differentiation) as Moderate. But ISO 9001 is a baseline operational certification — it does not evidence differentiation. True differentiation is patents, DSIR recognition, USFDA/EU-GMP, proprietary product lines, specialized equipment. Auto-QA flag: C3 = Moderate with only ISO 9001 as evidence.

2. **C4 false positives:** LLM infers "technical" from any engineering degree. A B.Tech from a tier-3 college running a commodity forging shop is not the same as an IIT-Bombay Chemical Engineering grad building specialty compounds. Calibration prompt engineering can reduce this, but human spot-check is still needed.

3. **C6 false positives:** LLM reads a press page and scores C6 (growth signals) as Moderate without verifying the article dates. A press page full of articles from 2019 is actually a C6 = Weak red flag — no activity in 5+ years. Auto-QA flag: C6 evidence that references any date before 2023.

4. **C1 false negatives:** Some manufacturers use "solutions" or "services" language on their website (to appeal to enterprise customers) but actually manufacture. LLM takes website language too literally and scores E1 = FAIL. These need human review — especially in B2B industrial segments.

### QA Process

**Step 1 — Automated QA flags (programmatic, before human review):**
- Any C3 evidence mentioning only "ISO 9001" without other differentiators → flag
- Any C6 evidence with dates before January 2023 → flag
- Any company with C1 = FAIL but website contains "manufacturing" + "plant" + "facility" in same paragraph → flag as potential false negative
- Any company with all 6 scores = Strong (total 100/100) → spot-check 20 random ones

**Step 2 — Human QA on flagged companies (~400–500 companies):**
- 3–4 minutes per company: open website, verify 2–3 key claims, correct misscored criteria
- Pace: 20–25 companies/hour → ~20 hours of human QA across week 3–4
- Decision: Accept, Reject, or Reclassify (Strong Pass → Pass, Pass → Borderline, etc.)

**Step 3 — Final list assembly:**
- All Strong Pass (expected ~700–800 after QA): include
- QA-verified Pass (expected ~300–400): include
- Remove all unresolved Borderline from the final 1,000 (they feed a secondary list)
- Target: **1,000 verified companies**

| Day | Task |
|-----|------|
| 19–20 | Run automated QA flags. Separate flagged from clean. |
| 20–24 | Human QA on ~400 flagged companies (2–3 hours/day × 4 days). |
| 24–25 | Spot-check 50 random Strong Pass companies. |
| 25–27 | Final assembly: merge clean Strong Pass + QA-verified Pass. Deduplicate. Verify count ≥ 1,000. |
| 27–28 | Add personalization hooks for top 200 (priority outreach tier) — one specific recent detail per company for line 1 of outreach email. |
| 28–29 | Format final deliverable: master CSV + summary dashboard + this methodology document. |
| 30 | Buffer day for overruns, data gaps, or yield shortfalls. |

---

## Weekly Summary

| Week | Focus | Output |
|------|-------|--------|
| 1 | Sourcing | 3,300–3,500 company universe with names, cities, segment tags, websites. Hard pre-filtered to ~2,200–2,500. |
| 2 | Scraping + first-pass scoring | All companies scraped. Haiku scores all. First-pass results: ~1,100–1,300 passes. |
| 3 | Borderline re-scoring + QA start | Sonnet re-scores borderlines. Human QA begins on flagged companies. |
| 4 | QA completion + final assembly | 1,000 verified companies in final CSV. Top 200 with personalization hooks. |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Yield lower than 30% | Expand universe: add state-level industrial directories (TSIIC, MIDC state lists), Google Maps scraping for companies in MIDC/GIDC estates, contact 2–3 industry association offices directly for member lists. |
| Scrapers blocked | Rotate user-agents and add randomized delays. Use residential proxy for high-value blocked sites. Fall back to manual research for top-priority companies that block scraping. |
| AI scoring accuracy < 80% | Re-calibrate prompt on 30-company test set. Split scoring: Haiku for C1/C2/C5/C6 (factual, date-checkable), Sonnet for C3/C4/C7/C8 (judgment, nuanced). |
| QA takes longer than 20 hours | Tighten auto-QA rules to reduce human review load. Accept that some borderline companies will remain unreviewed — add them to a secondary "needs more research" list rather than blocking the primary 1,000. |
| Deduplication errors | Use fuzzy string matching (RapidFuzz in Python) + CIN number matching for listed companies. Manual review of top 50 suspected duplicates. |
| Yield rate on certain segments too low | If a segment (e.g., industrial instrumentation) consistently yields <20%, deprioritize it and expand higher-yield segments (specialty chemicals, pharma intermediates). Adapt the sourcing mix based on week-1 data. |

---

## Tools and Budget

| Tool | Purpose | Estimated Cost |
|------|---------|----------------|
| Claude Haiku API | First-pass ICP scoring (2,500 companies) | ~Rs.1,050 |
| Claude Sonnet API | Borderline re-scoring (500 companies) | ~Rs.1,680 |
| Antigravity | MCA data extraction, company discovery | Licence provided |
| Playwright + Python | Website scraping | Free (open source) |
| GitHub Copilot | Code assistance for scraper + pipeline | Licence provided |
| LinkedIn Sales Navigator | DM discovery, company enrichment (optional) | Licence provided |
| Tofler / Zauba Corp | Revenue estimates for private companies | ~Rs.2,000 (spot queries) |
| PostgreSQL / Google Sheets | Master data storage + QA tracking | Free |
| **Total AI + data cost** | | **~Rs.5,000** |

---

## Final Deliverable

1. **Master CSV** — 1,000 companies, each with: name, website, city, segment, what they make, revenue band, decision-maker, E1/E2 status, C3–C8 scores with one-line evidence, verdict, confidence flags
2. **Priority-200 list** — top 200 companies sorted by Federer Score with personalization hooks ready for outbound emails
3. **Methodology document** — sources used, scraper architecture, scoring prompt, QA process, yield rates at each stage
4. **Code repository** — scraper scripts, scoring pipeline, deduplication notebook, QA flagging logic — all reproducible
5. **Source breakdown** — which of the 7 sources contributed how many final-list companies (to optimize future sourcing investment)
