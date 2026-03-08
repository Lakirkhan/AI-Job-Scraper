# 🏗️ System Architecture & Data Flow

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Job Scraper System                       │
└─────────────────────────────────────────────────────────────────┘

                              main.py
                              (Orchestrator)
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              ┌─────▼──────┐  ┌──▼──┐  ┌──────▼─────┐
              │  Scraping  │  │Filter│  │  Export   │
              │   Layer    │  │ Layer │  │   Layer   │
              └──────┬──────┘  └──┬──┘  └──────┬─────┘
                    │             │            │
              ┌─────▼──────┐     │       ┌─────▼─────┐
              │ 9 Scrapers │     │       │  Exporters│
              └──────┬──────┘     │       └─────┬─────┘
                    │             │            │
          ┌─────────┼─────────┬───┼──┐     ┌───┼────┬────┐
          │         │         │   │  │     │   │    │    │
    ┌─────▼──┐ ┌───▼───┐ ┌──▼─┐│ │  │ ┌──▼──┐│ ┌─▼──┐│
    │LinkedIn│ │Naukri │ │...││ │  │ │Excel││ │CSV ││
    └────────┘ └───────┘ └────┘│ │  │ └─────┘│ └────┘│
          ▲         ▲         ▲ │ │  │       ▲       ▲
          │         │         │ │ │  │       │       │
         Raw Job Data (Standardized Format)   │       │
                    │                         │       │
              ┌─────▼─────────────────────────┼───────┼─────┐
              │                               │       │     │
         ┌────▼──────┐            ┌──────────▼──┐ ┌──▼──┐ │
         │Deduplication           │SkillFilter  │ │Email│ │
         │(Remove duplicates)     │(30+ skills) │ │Alert│ │
         └────┬──────┘            └──────────┬──┘ └──┬──┘ │
              │                        │          │   │    │
         ┌────▼────────────────────────▼──────────┼───┼────┐
         │    Filtered & Cleaned Job List         │   │    │
         ├────────────────────────────────────────┼───┼────┤
         │    • No Duplicates                      │   │    │
         │    • Matched Skills Only                │   │    │
         │    • Standardized Format               │   │    │
         └────────────────────────────────────────┴───┴────┘
                          ▲
                          │
                    ┌─────▼─────┐
                    │Config.py   │
                    │(Settings)  │
                    └────────────┘
```

---

## Data Flow Architecture

### 1️⃣ **Scraping Phase**

```
┌──────────────────────────────────────────┐
│  Scraper Classes (linkedin_scraper.py)   │
├──────────────────────────────────────────┤
│                                          │
│  1. Send HTTP request with headers       │
│  2. Parse HTML with BeautifulSoup        │
│  3. Extract job cards using CSS selectors│
│  4. Parse individual job details         │
│  5. Format to standard dict              │
│  6. Handle errors & retries              │
│                                          │
│  Return: List[Dict] - Standardized jobs  │
└──────────────────────────────────────────┘
                    │
                    ▼
            Raw Job Data (127 jobs)
```

### 2️⃣ **Deduplication Phase**

```
┌──────────────────────────────────────────┐
│  Deduplication (deduplication.py)        │
├──────────────────────────────────────────┤
│                                          │
│  Compare jobs by:                        │
│  - Job Title                             │
│  - Company Name                          │
│  - Location                              │
│                                          │
│  Remove: 5 duplicate jobs                │
│  Keep: 122 unique jobs                   │
│                                          │
└──────────────────────────────────────────┘
                    │
                    ▼
        Unique Job Data (122 jobs)
```

### 3️⃣ **Filtering Phase**

```
┌──────────────────────────────────────────┐
│  Skill Filter (skill_filter.py)          │
├──────────────────────────────────────────┤
│                                          │
│  For each job, check if title/desc       │
│  contains at least ONE required skill:   │
│                                          │
│  JOB_SKILLS = [                          │
│    "react", "python", "machine learning" │
│    "data science", "typescript", ...     │
│  ]                                       │
│                                          │
│  Match: 45 jobs have required skills     │
│  Filter: 77 jobs without required skills │
│                                          │
└──────────────────────────────────────────┘
                    │
                    ▼
        Filtered Job Data (45 jobs)
```

### 4️⃣ **Export Phase**

```
┌──────────────────────────────────────────┐
│  Excel Exporter (export_excel.py)        │
├──────────────────────────────────────────┤
│                                          │
│  ✓ Create DataFrame from jobs            │
│  ✓ Format headers (blue, bold, white)    │
│  ✓ Auto-size columns                     │
│  ✓ Add borders and alignment             │
│  ✓ Save to output folder                 │
│                                          │
│  Output: jobs_20260308_1308.xlsx         │
│                                          │
└──────────────────────────────────────────┘
                 │         │
        ┌────────┘         └────────┐
        ▼                           ▼
    [ .xlsx ]                   [ .csv ]
     (Excel)              (Comma Separated)
```

### 5️⃣ **Email Phase**

```
┌──────────────────────────────────────────┐
│  Email Sender (email_sender.py)          │
├──────────────────────────────────────────┤
│                                          │
│  1. Create HTML email template           │
│  2. Format jobs with details             │
│  3. Batch if needed (5 jobs per email)   │
│  4. Connect to Gmail SMTP (port 587)     │
│  5. Login with app password              │
│  6. Send email(s) with MIMEMultipart     │
│  7. Handle errors gracefully             │
│                                          │
│  Output: HTML emails to recipient        │
│                                          │
└──────────────────────────────────────────┘
                    │
                    ▼
            Email Sent ✓
```

---

## Component Interaction Diagram

```
                    ┌─────────────┐
                    │   main.py   │
                    │(Orchestrator)
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐       ┌──────────┐      ┌──────────┐
    │Scrapers│       │Filters   │      │Export    │
    └────┬───┘       └────┬─────┘      └────┬─────┘
         │                │                  │
    ┌────▼────┐      ┌────▼─────┐      ┌────▼─────┐
    │config.py│      │config.py  │      │config.py  │
    └─────────┘      └───────────┘      └───────────┘
         │                │                  │
    ┌────▼────────────────▼──────────────────▼─────┐
    │           Utilities (utils/)                  │
    ├───────────────────────────────────────────────┤
    │  • database.py      (DB helpers)              │
    │  • deduplication.py (Remove duplicates)       │
    │  • email_sender.py  (Email alerts)            │
    │  • export_excel.py  (Excel format)            │
    │  • csv_exporter.py  (CSV format)              │
    └───────────────────────────────────────────────┘
```

---

## Job Data Format (Throughout System)

```python
job = {
    'title': 'Senior Python Developer',          # Job title
    'company': 'Tech Corp Inc.',                 # Company name
    'location': 'San Francisco, CA',             # Job location
    'salary': '$150,000 - $180,000',             # Salary range
    'description': 'Looking for experienced...', # Job description (optional)
    'link': 'https://company.com/job/123',      # Apply link
    'source': 'LinkedIn',                        # Source website
    'date_scraped': '2026-03-08 13:08:45'       # When job was scraped
}
```

**Standardization ensures:**
- Consistent data across all scrapers
- Easy filtering and sorting
- Simple export to Excel/CSV
- Email formatting

---

## Configuration & Dependency Flow

```
┌─────────────────────────────────────┐
│        config.py (Central)          │
├─────────────────────────────────────┤
│  EMAIL         ──► email_sender.py   │
│  PASSWORD                            │
│  RECIPIENT_EMAIL                     │
│                                      │
│  JOB_SKILLS    ──► skill_filter.py   │
│  LOCATION                            │
│  SEARCH_QUERIES                      │
│                                      │
│  TIMEOUT       ──► all_scrapers.py   │
│  MAX_RETRIES                         │
│  USER_AGENT                          │
│                                      │
│  SCHEDULE_TIME ──► main.py           │
│  ENABLE_SCHEDULER                    │
│                                      │
│  OUTPUT_FOLDER ──► exporters.py      │
│  EXCEL_PREFIX                        │
│  CSV_PREFIX                          │
│                                      │
└─────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────┐
│  Each Scraper/Component     │
└────────────┬────────────────┘
             │
        ┌────▼──────────┐
        │ Try Operation │
        └────┬──────────┘
             │
    ┌────────┴────────┐
    │                 │
NO  ▼                 ▼  YES
┌────────────┐   ┌─────────┐
│ Catch      │   │ Success │
│ Exception  │   │ Return  │
└────┬───────┘   └─────────┘
     │
┌────▼──────────────┐
│ Log Error Message │
│ (Graceful Error)  │
└────┬──────────────┘
     │
┌────▼──────────────┐
│ Continue (Don't   │
│ Crash System)     │
└───────────────────┘
```

---

## Scheduling Flow (Optional)

```
┌─────────────────────────────────┐
│  main.py starts                 │
│  (Scheduler mode enabled)       │
└────────────┬────────────────────┘
             │
        ┌────▼──────────────┐
        │ Schedule task to  │
        │ run at SCHEDULE_  │
        │ TIME daily        │
        └────┬──────────────┘
             │
    ┌────────▼────────┐
    │ Loop: Check     │
    │ every 60 sec    │
    └────┬────────────┘
         │
    ┌────▼──────────────────┐
    │ Is it scheduled time? │
    ├────────────┬──────────┤
    │ NO: Wait   │ YES: Run │
    │            │          │
    └────────────┴──┬───────┘
                    │
            ┌───────▼────────┐
            │ Execute run_once│
            │ (Full scrape)   │
            └────┬───────────┘
                 │
            ┌────▼───────────┐
            │ Tomorrow...    │
            │ Check again    │
            └────────────────┘
```

---

## Performance Optimization

```
┌─────────────────────────────────┐
│  Performance Characteristics    │
├─────────────────────────────────┤
│                                 │
│  Scraping:        30-60 sec     │
│  • 9 sites × 2 sec delay        │
│  • Network latency              │
│  • HTML parsing                 │
│                                 │
│  Deduplication:   <1 sec        │
│  • Set comparison               │
│  • Single pass                  │
│                                 │
│  Filtering:       ~1 sec        │
│  • String matching              │
│  • Simple logic                 │
│                                 │
│  Export:          1-2 sec       │
│  • DataFrame creation           │
│  • File I/O                     │
│  • Formatting                   │
│                                 │
│  Email:           5-10 sec      │
│  • SMTP connection              │
│  • HTML generation              │
│                                 │
│  TOTAL:           ~2 minutes    │
│  (per full run)                 │
│                                 │
└─────────────────────────────────┘
```

---

## Class Inheritance & Composition

```
┌──────────────────────────────────┐
│  Scraper Base Pattern (All)      │
├──────────────────────────────────┤
│ • __init__() - Setup headers/URL │
│ • scrape()   - Main method       │
│ • _parse_job_card() - Parse HTML │
│ Return: List[Dict]               │
└──────────────────────────────────┘
           ▲
           │ Similar Pattern
           │
  ┌────────┼────────┬────────┬──────┬──────┐
  │        │        │        │      │      │
  │   LinkedIn  Naukri  Indeed  ...  Foundit
  
┌──────────────────────────────────┐
│  Filter Pattern (skill_filter)   │
├──────────────────────────────────┤
│ • __init__() - Load skills       │
│ • filter_jobs() - Main method     │
│ • _matches_skills() - Check match │
│ Return: List[Dict]               │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  Exporter Pattern (Excel/CSV)    │
├──────────────────────────────────┤
│ • __init__() - Setup paths       │
│ • export() - Main method          │
│ • format/parse() - Specifics     │
│ Return: filepath                 │
└──────────────────────────────────┘
```

---

## Summary

The system is designed with:

✅ **Modularity** - Each component is independent
✅ **Reusability** - Classes and functions designed for extension
✅ **Scalability** - Easy to add new scrapers
✅ **Resilience** - Error handling throughout
✅ **Performance** - Optimized for quick execution
✅ **Maintainability** - Clear structure and documentation

**Result:** A professional, production-ready job scraping system! 🚀

