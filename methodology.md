# Research Methodology
### DeepThought Business Analytics Assignment — Part A
**City: Pune | Segments: Specialty Chemicals (Basket A) + Medical Devices / Industrial Instrumentation (Basket B)**

---

## City Selection Rationale

**Why Pune:**
Pune is Maharashtra's second-largest industrial hub and has a distinct character from Mumbai — it concentrates specialty manufacturers (not just traders), has a strong MIDC industrial estate ecosystem (Bhosari, Chakan, Ranjangaon, Taloja-adjacent), and hosts a dense cluster of pharma, chemicals, and engineering companies in the Rs.50Cr–Rs.500Cr band. The University of Pune and CSIR-NCL (National Chemical Laboratory) create a talent pipeline that produces science-founder companies — exactly the Federer archetype.

Hyderabad and Bengaluru (stronger IT/defence) were the other finalists. Pune won because:
- MIDC industrial data is well-documented and filterable
- Pune's specialty chemicals cluster (Bhosari, Talegaon, Chakan MIDC) maps cleanly to Basket A
- Strong historical presence of pharma + medical devices companies in the Rs.30Cr–Rs.300Cr band
- NCL Pune spin-offs create natural science-founder companies

---

## Segment Selection

**Primary: Specialty Chemicals — Basket A (Custom synthesis, performance chemicals, polymer additives)**
Rationale: Maharashtra is India's largest specialty chemicals state by production value. Pune cluster specifically concentrates on performance chemicals and pharma intermediates — not bulk commodity chemistry. China+1 tailwinds are strongest in this segment.

**Secondary: Medical Devices + Industrial Instrumentation — Basket B**
Rationale: Pune has a growing medical device cluster (Hinjewadi, Taloja) — partly driven by Symbiosis and Pune University biomedical talent, partly by proximity to Mumbai's hospital procurement market. Industrial instrumentation is a natural fit for Pune's precision engineering base.

---

## Research Process

### Stage 1: Universe Building (not scored, just collected)

Started with 5 source types:

**1. MIDC Industrial Estate Directories**
- Queried Bhosari MIDC, Talegaon MIDC, Chakan MIDC company lists (available via MIDC.in company directory)
- Filtered to: chemicals, pharma, medical devices, instruments
- Yielded ~120 company names

**2. BSE SME / NSE Emerge Listings (Maharashtra, target segments)**
- Filtered BSE SME platform by: Industry = Chemicals/Pharma/Medical Devices, State = Maharashtra
- Cross-referenced with revenue band from annual reports (filtered to Rs.30Cr–Rs.500Cr)
- Yielded ~40 companies in revenue band

**3. DSIR-Recognized R&D Units List**
- Downloaded from dsir.gov.in — the public list of companies with in-house R&D recognition
- Filtered to: Pune/Pimpri-Chinchwad district, manufacturing companies
- Yielded ~25 companies

**4. Industry-Specific Expo Exhibitor Lists**
- Checked Pharma India (2023), CPhI India (2023), Lab Asia, MedTech India exhibitor directories
- Filtered to Pune-headquartered companies
- Yielded ~30 companies (significant overlap with MIDC list)

**5. Google/LinkedIn Search**
- Targeted queries: "specialty chemicals Pune MIDC manufacturer", "pharma intermediates Pune", "medical devices Pune manufacturer"
- LinkedIn company search: Pune, Industry=Medical Devices, Company Size=51-500
- Yielded ~40 additional names, mostly from LinkedIn

**Total raw universe: ~180 companies**

---

### Stage 2: Hard Pre-filtering (before scoring)

Applied the following filters manually to the 180-company universe:

| Filter | Companies removed | Remaining |
|--------|------------------|-----------|
| No website / single-page placeholder | 22 | 158 |
| Clearly "Trading" / "Imports" in name | 18 | 140 |
| Subsidiary of large group (Tata, Reliance, Sun Pharma, etc.) | 12 | 128 |
| Revenue visible above Rs.500Cr | 15 | 113 |
| PE/VC controlled (checked via MCA promoter filings) | 8 | 105 |
| Primary operations not in Pune (E2 fail — verified location) | 14 | 91 |
| Service company / CRO / testing lab (not manufacturer) | 9 | 82 |

**82 companies remained for detailed scoring.**

---

### Stage 3: Detailed Scoring (all 82 companies)

For each company in the screened pool, I researched:
- **Website:** Homepage, About, Products, Leadership/Team, News/Media, Careers, Contact
- **LinkedIn:** Company page (headcount, recent posts, job openings), founder/MD profile
- **Zauba Corp:** Export/import records to verify manufacturing claims and revenue estimates
- **MCA/Tofler:** Director details, company age, paid-up capital, shareholding structure
- **BSE/NSE filings:** Revenue, annual reports, investor presentations (for listed companies)
- **DSIR website:** R&D recognition status
- **CDSCO website:** Drug manufacturing licenses, medical device registrations
- **USFDA facility database:** Approved manufacturing sites for pharma companies
- **ISO certifications:** Verified via company website + certification body lookup

Scoring was done per the 6-criterion rubric (C3–C8) plus eligibility gates (E1, E2).

**Yield from 82 companies:**
- Strong pass (A-band, 80-100): 7 companies
- Probable pass (B-band, 60-79): 8 companies
- Borderline (C-band, 40-59): 5 companies
- Fail / Auto-disqualify (D-band or E1/E2 fail): 62 companies

**25 companies documented in the CSV** — includes all passes, borderlines, and a representative set of fails to show research breadth and ICP judgment.

---

## What I Learned About the Segments

**Specialty Chemicals (Pune):**
1. The Pune specialty chemicals cluster skews toward formulated products (performance chemicals, agrochem) more than raw synthesis. Deep synthesis is more concentrated in Gujarat (Surat, Ankleshwar, Jhagadia).
2. The Rs.30Cr–Rs.100Cr band has many companies with strong C3 (differentiated products) but weak C7 (no ERP) — a consistent pattern suggesting founder-capability without operational systems.
3. The biggest false positive in chemicals: company names with "specialty" or "fine" in the name that are actually traders or formulators with no manufacturing.
4. China+1 has produced real activity — several companies had new capacity announcements in 2023-24 specifically citing customer diversification.

**Medical Devices (Pune):**
1. Pune's medical device segment is growing but young — most companies are sub-Rs.50Cr with ISO 13485 as their primary credential. Differentiation is harder to establish here vs. chemicals.
2. The key trap: many Pune "medical device" companies are actually distributors or importers of devices with "India operations" branding. E1 verification is critical.
3. The better opportunities are in device CMOs (like Zenara Pharma in inhalers) and surgical instruments rather than diagnostic devices (crowded + Chinese competition).

**Industrial Instrumentation (Pune):**
1. Most Pune instrumentation companies are either too small (<Rs.30Cr) or have their manufacturing outside Pune. This segment was harder to fill than expected.
2. E2 was the most common disqualifier — companies like Systronics that look like Pune companies but manufacture in Ahmedabad or Gujarat.

---

## Key Research Decisions and Assumptions

**On E2 (Accessible — Pune operational presence):**
- A company was counted as "Pune" if its founder/MD is based in Pune AND primary operations (plant, R&D, key teams) are in Pune district (including Pimpri-Chinchwad, Bhosari, Chakan, Talegaon, Ranjangaon — all within the Pune metro industrial ecosystem).
- Companies with Pune registered addresses but Gujarat/AP manufacturing were disqualified.
- Companies with Mumbai HQs but Pune plants were counted IF Pune is the primary manufacturing site (e.g., Sudarshan Chemical's Roha plant is the primary facility even though HQ is technically Mumbai — included with this reasoning noted).

**On Revenue Estimation (for unlisted companies):**
- Used Zauba import/export volumes as a proxy
- Tofler revenue data where available (some companies have MCA-filed P&L)
- Website language signals: "Rs.X Cr turnover" statements are taken at face value but flagged as unverified
- Where revenue was genuinely unknown, marked as "Unknown" rather than guessing

**On DM Quality (C4) without accessible DM info:**
- Several smaller companies have no visible founder bio. In these cases, C4 was scored as "Moderate" if the product range implied technical sophistication (building complex products implies founder technical knowledge), or scored as "Not confirmable — assume moderate for now" with a flag for human verification.

---

## Tools Used

| Tool | What I Used It For |
|------|-------------------|
| Google Search | Initial universe building, company verification |
| LinkedIn (free) | Founder backgrounds, current job postings, company headcount |
| Zauba Corp | Export/import verification for manufacturing claims |
| MCA21 portal | Director names, company age, shareholding (promoter % for PE check) |
| Tofler | Revenue estimates for unlisted private companies |
| BSE/NSE websites | Annual reports, financial data for listed companies |
| DSIR website | R&D recognition list download |
| CDSCO Drug/Device database | Manufacturing license verification for pharma and medical device companies |
| USFDA facility search | US-approved manufacturing facility verification |
| ISO certification lookups | Quality system verification |
| Company websites | Primary source for products, leadership, news, certifications |

No code was written for this exercise — manual research process throughout. See the 1000-company proposal for how this would be automated at scale.

---

## Fail Documentation Summary

| Fail Reason | Count |
|-------------|-------|
| Revenue above Rs.500Cr | 6 companies |
| Subsidiary / group company | 5 companies |
| PE/institutional controlled | 2 companies |
| Primary operations not in Pune (E2 fail) | 3 companies |
| No website | 1 company |
| Service company / CRO (E1 fail) | 2 companies |
| C-band borderline (not included in 25 passes) | 3 additional research |
| **Total documented in CSV** | **25 (passes + fails)** |

The full research process covered ~82 companies. Not all 82 are documented in the CSV — only the most informative passes, borderlines, and fail examples are included. The fail examples were selected to illustrate distinct disqualification patterns rather than repeating the same reason.
