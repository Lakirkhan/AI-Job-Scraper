# AI-Powered Job Scraper System

A comprehensive Python-based job scraping solution that automatically discovers and aggregates job listings from multiple job platforms, filters them by skills, and sends automated email alerts.

**Status:** Production Ready | **Version:** 2.0

---

## Table of Contents

- [Features](#features)
- [Supported Job Platforms](#supported-job-platforms)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Email Setup](#email-setup)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Core Features
- **Multi-Platform Scraping** - Scrapes 9+ major job platforms simultaneously
- **Intelligent Skill Filtering** - Filters jobs based on 30+ technology skills
- **Automatic Deduplication** - Removes duplicate listings from multiple sources
- **Email Alerts** - Sends formatted HTML email notifications
- **Multi-Format Export** - Excel (.xlsx) and CSV (.csv) exports
- **Daily Scheduling** - Automatic daily scraping at set time
- **Error Handling** - Robust retry logic and error management
- **Modular Architecture** - Easy to extend with new scrapers

### Advanced Features
- **Rate-Limited Requests** - Respects server limits with delays
- **Formatted Excel** - Color-coded headers, auto-sized columns
- **Batch Email Processing** - Sends job alerts in logical batches
- **Secure Credentials** - App password support for Gmail
- **Responsive Design** - Clean, formatted HTML emails
- **Flexible Filtering** - Custom skill lists support

---

## Supported Job Platforms

1. **LinkedIn** - World's largest professional network
2. **Naukri** - Most popular in India
3. **Indeed** - Global job board
4. **Glassdoor** - Company reviews + jobs
5. **Wellfound** (AngelList) - Startup jobs
6. **Monster** - Classic job portal
7. **TimesJobs** - Popular in India
8. **Internshala** - Internships & entry-level
9. **Foundit** - Indian job portal

---

## Technology Stack

**Python Libraries:**
- `requests` - HTTP requests
- `BeautifulSoup4` - Web scraping
- `pandas` - Data manipulation
- `openpyxl` - Excel file handling
- `lxml` - XML parsing
- `schedule` - Job scheduling
- `smtplib` - Email sending

**Supported Python Versions:** 3.8+

---

## Project Structure

```
job-scraper/
├── main.py                          # Main orchestrator
├── setup.py                         # Interactive setup script
├── requirements.txt                 # Dependencies
├── README.md                        # This file
├── QUICKSTART.md                    # Quick start guide
├── ARCHITECTURE.md                  # System design
├── IMPLEMENTATION_SUMMARY.md        # Project overview
├── PROJECT_COMPLETE.md              # Setup instructions
├── .gitignore                       # Git ignore file
│
├── scrapers/                        # Web scrapers
│   ├── google_search_scraper.py    # Google search discovery
│   ├── linkedin_scraper.py         # LinkedIn scraper
│   ├── naukri_scraper.py           # Naukri scraper
│   ├── indeed_scraper.py           # Indeed scraper
│   ├── glassdoor_scraper.py        # Glassdoor scraper
│   ├── wellfound_scraper.py        # Wellfound scraper
│   ├── monster_scraper.py          # Monster scraper
│   ├── timesjobs_scraper.py        # TimesJobs scraper
│   ├── internshala_scraper.py      # Internshala scraper
│   └── foundit_scraper.py          # Foundit scraper
│
├── filters/                         # Data processing
│   └── skill_filter.py             # Job skill filtering
│
├── utils/                           # Utilities
│   ├── config.py                   # Configuration & constants
│   ├── email_sender.py             # Email notifications
│   ├── export_excel.py             # Excel export
│   ├── csv_exporter.py             # CSV export
│   ├── deduplication.py            # Duplicate removal
│   └── database.py                 # Database utilities
│
└── output/                          # Generated files
    ├── jobs_20260308_1308.xlsx     # Excel exports
    ├── jobs_20260308_1308.csv      # CSV exports
    └── ...

```

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Lakirkhan/AI-Job-Scraper.git
cd AI-Job-Scraper
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers (Optional for advanced scraping)
```bash
playwright install
```

---

## Configuration

### 1. Update `utils/config.py`

```python
# Email Configuration
EMAIL = "your-email@gmail.com"           # Your Gmail address
PASSWORD = "your-app-password"           # Gmail App Password (not regular password)
RECIPIENT_EMAIL = "recipient@gmail.com"  # Email to receive alerts

# Job Scraping Configuration
SEARCH_QUERIES = [
    "React developer jobs",
    "Node.js developer jobs",
    "Python developer jobs",
    "AI engineer jobs",
    "Machine learning engineer jobs",
    "software developer jobs remote",
    "Full stack developer jobs",
    "Data Science jobs"
]

# Required Skills Filter
JOB_SKILLS = [
    "react",
    "react.js",
    "node.js",
    "nodejs",
    "python",
    "django",
    "flask",
    "php",
    "laravel",
    "ai",
    "artificial intelligence",
    "machine learning",
    "data science",
    "backend",
    "frontend",
    "full stack",
    "typescript",
    "javascript",
    "java",
    ".net",
    "c#",
    "mongodb",
    "sql",
    "postgresql",
    "mysql",
    "redis",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git"
]

LOCATION = "India"  # Can be changed to any location

# Scraper Configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TIMEOUT = 30  # Seconds
MAX_RETRIES = 3

# Google Search Configuration
GOOGLE_SEARCH_RESULTS_PER_QUERY = 5  # Number of URLs to extract from each Google search

# Output Configuration
OUTPUT_FOLDER = "output"
EXCEL_PREFIX = "jobs_"
CSV_PREFIX = "jobs_"

# Scheduler Configuration
SCHEDULE_TIME = "09:00"  # Time to run scheduler daily (HH:MM format)
ENABLE_SCHEDULER = True

# Database Configuration (for deduplication)
DUPLICATE_CHECK_FIELDS = ["title", "company", "location"]

# Email Configuration for Alerts
SEND_EMAIL_ALERTS = True
JOBS_PER_EMAIL = 5  # Maximum jobs to include in one email
```

### 2. Required Skills Configuration

The filter includes 30+ technologies by default:
- **Frontend:** React, React.js, Vue, Angular, TypeScript, JavaScript
- **Backend:** Node.js, Python, Django, Flask, PHP, Laravel, Java, .NET, C#
- **Data:** AI, Machine Learning, Data Science, SQL, MongoDB, PostgreSQL
- **DevOps:** Docker, Kubernetes, AWS, Azure, GCP, Git, Redis

**Edit skills in `utils/config.py`** to customize.

---

## Usage

### Run Once (Single Execution)
```bash
python main.py
```

The system will:
1. Scrape all 9 job platforms
2. Remove duplicates
3. Filter by required skills
4. Export to Excel & CSV
5. Send email alerts

### Run Scheduled Daily
```bash
# Ensure ENABLE_SCHEDULER = True in config.py
python main.py
```

The process will run daily at the configured time (`SCHEDULE_TIME` in config.py).

### Expected Output
```
============================================================
Starting Job Scraper - 2026-03-08 13:30:45
============================================================

Scraping LinkedIn...
✓ LinkedIn: Scraped 12 jobs
Scraping Naukri...
✓ Naukri: Scraped 18 jobs
[... more scrapers ...]

✓ Total Jobs Scraped: 127

Removing duplicates...
ℹ Removed 5 duplicate jobs
✓ Jobs after deduplication: 122

Filtering by required skills...
ℹ Skill Filter: 45/122 jobs matched (77 filtered out)
✓ Filtered Jobs: 45

Exporting jobs...
✓ Excel exported: output/jobs_20260308_1330.xlsx (45 jobs)
✓ CSV exported: output/jobs_20260308_1330.csv (45 jobs)

Sending email alerts...
✓ Email alerts sent

============================================================
Scraper Completed - 2026-03-08 13:30:52
============================================================
```

---

## Email Setup

### Getting Gmail App Password

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Settings](https://myaccount.google.com/security)
   - Find "2-Step Verification" and enable it

2. **Generate App Password**
   - In Security settings, find "App Passwords"
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password

3. **Update Config**
   ```python
   EMAIL = "your-email@gmail.com"
   PASSWORD = "abcdefghijklmnop"  # Your 16-character app password
   ```

### Email Features
- Formatted HTML emails with job details
- Direct "Apply Now" links
- Job information: Title, Company, Location, Salary, Source
- Batch sending for large job lists

### Example Email Content
```
Job Title: Senior Python Developer
Company: Tech Corp Inc.
Location: San Francisco, CA
Salary: $120,000 - $160,000
Source: LinkedIn

[Apply Now Button]
```

---

## Output

### Excel File
- **Location:** `output/jobs_YYYYMMDD_HHMM.xlsx`
- **Features:**
  - Formatted headers (blue background, white text)
  - Auto-sized columns
  - All job details included
  - Ready for analysis

### CSV File
- **Location:** `output/jobs_YYYYMMDD_HHMM.csv`
- **Features:**
  - Standard CSV format
  - Compatible with any spreadsheet
  - Easy to import into databases

### Sample Data
| Title | Company | Location | Salary | Source | Date Scraped |
|-------|---------|----------|--------|--------|--------------|
| Senior Python Dev | Tech Corp | SF, CA | $150K | LinkedIn | 2026-03-08 |
| React Engineer | Startup XY | Remote | $130K | Wellfound | 2026-03-08 |

---

## Advanced Configuration

### Custom Search Locations
```python
# In utils/config.py
LOCATION = "San Francisco"   # Change to your target location
```

### Email Batch Size
```python
JOBS_PER_EMAIL = 5  # Number of jobs per email alert
```

### Scraper Timeout
```python
TIMEOUT = 30  # Seconds to wait for response
MAX_RETRIES = 3  # Number of retry attempts
```

### Duplicate Detection Fields
```python
DUPLICATE_CHECK_FIELDS = ["title", "company", "location"]
```

---

## Troubleshooting

### Email Not Sending
**Error:** `SMTPAuthenticationError: Username and Password not accepted`

**Solution:**
1. Use Gmail App Password (not regular password)
2. Enable 2-Factor Authentication
3. Verify `EMAIL` and `PASSWORD` in config.py
4. Check if "Less secure app access" is disabled (recommended)

### No Jobs Found
**Possible Causes:**
1. Website structure changed (selectors may be outdated)
2. Website blocked scraping (use VPN or residential proxies)
3. Network connectivity issues

**Solutions:**
1. Update selectors in specific scraper files
2. Check user-agent in config.py
3. Verify internet connection

### Low Filtered Results
**Possible Causes:**
1. Search skills too restrictive
2. Search queries not matching job market
3. Location filtering too narrow

**Solutions:**
1. Add more skills to `JOB_SKILLS` in config.py
2. Diversify `SEARCH_QUERIES`
3. Change `LOCATION` or remove location filter

### Scheduler Not Running
**Solution:**
```bash
# Make sure scheduler is enabled
ENABLE_SCHEDULER = True  # in config.py

# Run in background (Windows)
python main.py &

# Or use Windows Task Scheduler to run daily
```

---

## Performance Tips

1. **Optimize Search Queries** - Specific queries return better results
2. **Adjust Skill List** - Fewer skills = more results, but less relevant
3. **Increase Retry Attempts** - For unstable connections
4. **Schedule Off-Peak** - Run scraper during off-peak hours
5. **Use Filtering** - Filter by location to reduce results

---

## Contributing

Contributions are welcome! To add support for a new job platform:

1. Create new scraper in `scrapers/new_platform_scraper.py`
2. Implement `NewPlatformScraper` class with `scrape()` method
3. Return list of dictionaries with keys: `title`, `company`, `location`, `salary`, `link`, `source`, `date_scraped`
4. Add to scraper list in `main.py`
5. Test thoroughly
6. Submit pull request

### Example Scraper Template
```python
class NewPlatformScraper:
    def scrape(self, query="software developer", location=""):
        jobs = []
        # Your scraping logic here
        return jobs
```

---

## Legal & Ethics

- Respects website `robots.txt` and Terms of Service
- Implements rate limiting and delays
- Uses proper User-Agent headers
- Not intended for commercial resale
- Personal/research use recommended

*Always check website Terms of Service before scraping.*

---

## License

MIT License - Feel free to use and modify

---

## Roadmap

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web dashboard for job browsing
- [ ] Advanced filtering (salary range, experience level)
- [ ] Custom notifications (Slack, Discord, Telegram)
- [ ] Resume matching based on job descriptions
- [ ] Mobile app for job alerts
- [ ] Machine learning for job relevance ranking

---

## Acknowledgments

- Built with Python
- Inspired by best practices in web scraping
- Community feedback and contributions

---

## Support

For issues, questions, or suggestions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review `utils/config.py` for configuration tips
3. Check selector accuracy in scraper files
4. Submit issue with error details

---

**Last Updated:** March 8, 2026
**Version:** 2.0 (Production Ready)


2. **Naukri** - Most popular in India
3. **Indeed** - Global job board
4. **Glassdoor** - Company reviews + jobs
5. **Wellfound** (AngelList) - Startup jobs
6. **Monster** - Classic job portal
7. **TimesJobs** - Popular in India
8. **Internshala** - Internships & entry-level
9. **Foundit** - Indian job portal

---

## 🛠️ Technology Stack

**Python Libraries:**
- `requests` - HTTP requests
- `BeautifulSoup4` - Web scraping
- `pandas` - Data manipulation
- `openpyxl` - Excel file handling
- `lxml` - XML parsing
- `schedule` - Job scheduling
- `smtplib` - Email sending

**Supported Python Versions:** 3.8+

---

## 📁 Project Structure

```
job-scraper/
├── main.py                          # Main orchestrator
├── requirements.txt                 # Dependencies
├── README.md                        # This file
│
├── scrapers/                        # Web scrapers
│   ├── google_search_scraper.py    # Google search discovery
│   ├── linkedin_scraper.py         # LinkedIn scraper
│   ├── naukri_scraper.py           # Naukri scraper
│   ├── indeed_scraper.py           # Indeed scraper
│   ├── glassdoor_scraper.py        # Glassdoor scraper
│   ├── wellfound_scraper.py        # Wellfound scraper
│   ├── monster_scraper.py          # Monster scraper
│   ├── timesjobs_scraper.py        # TimesJobs scraper
│   ├── internshala_scraper.py      # Internshala scraper
│   └── foundit_scraper.py          # Foundit scraper
│
├── filters/                         # Data processing
│   └── skill_filter.py             # Job skill filtering
│
├── utils/                           # Utilities
│   ├── config.py                   # Configuration & constants
│   ├── email_sender.py             # Email notifications
│   ├── export_excel.py             # Excel export
│   ├── csv_exporter.py             # CSV export
│   ├── database.py                 # Database utilities
│   ├── deduplication.py            # Duplicate removal
│   └── __pycache__/
│
└── output/                          # Generated files
    ├── jobs_20260308_1308.xlsx     # Excel exports
    ├── jobs_20260308_1308.csv      # CSV exports
    └── ...

```

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd job-scraper
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers (Optional for advanced scraping)
```bash
playwright install
```

---

## ⚙️ Configuration

### 1. Update `utils/config.py`

```python
# Email Configuration
EMAIL = "your-email@gmail.com"           # Your Gmail address
PASSWORD = "your-app-password"           # Gmail App Password (see Email Setup)
RECIPIENT_EMAIL = "your-email@gmail.com" # Where to receive alerts

# Search Queries
SEARCH_QUERIES = [
    "React developer jobs",
    "Python developer jobs",
    "Data Science jobs",
    # ... add more queries
]

# Required Skills Filter
JOB_SKILLS = [
    "react", "node.js", "python",
    "machine learning", "data science",
    # ... see full list in config.py
]

# Scheduling
SCHEDULE_TIME = "09:00"  # Daily run time (HH:MM format)
ENABLE_SCHEDULER = True   # True to run daily, False to run once
```

### 2. Required Skills Configuration

The filter includes 30+ technologies by default:
- **Frontend:** React, React.js, Vue, Angular, TypeScript, JavaScript
- **Backend:** Node.js, Python, Django, Flask, PHP, Laravel, Java, .NET, C#
- **Data:** AI, Machine Learning, Data Science, SQL, MongoDB, PostgreSQL
- **DevOps:** Docker, Kubernetes, AWS, Azure, GCP, Git, Redis

✏️ **Edit skills in `utils/config.py`** to customize.

---

## 🚀 Usage

### Run Once (Single Execution)
```bash
python main.py
```

The system will:
1. Scrape all 9 job platforms
2. Remove duplicates
3. Filter by required skills
4. Export to Excel & CSV
5. Send email alerts

### Run Scheduled Daily
```bash
# Ensure ENABLE_SCHEDULER = True in config.py
python main.py
```

The process will run daily at the configured time (`SCHEDULE_TIME` in config.py).

### Expected Output
```
============================================================
Starting Job Scraper - 2026-03-08 13:30:45
============================================================

Scraping LinkedIn...
✓ LinkedIn: Scraped 12 jobs
Scraping Naukri...
✓ Naukri: Scraped 18 jobs
[... more scrapers ...]

✓ Total Jobs Scraped: 127

Removing duplicates...
ℹ Removed 5 duplicate jobs
✓ Jobs after deduplication: 122

Filtering by required skills...
ℹ Skill Filter: 45/122 jobs matched (77 filtered out)
✓ Filtered Jobs: 45

Exporting jobs...
✓ Excel exported: output/jobs_20260308_1330.xlsx (45 jobs)
✓ CSV exported: output/jobs_20260308_1330.csv (45 jobs)

Sending email alerts...
✓ Email sent successfully

============================================================
Scraper Completed - 2026-03-08 13:30:52
============================================================
```

---

## 📧 Email Setup

### Getting Gmail App Password

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Settings](https://myaccount.google.com/security)
   - Find "2-Step Verification" and enable it

2. **Generate App Password**
   - In Security settings, find "App Passwords"
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password

3. **Update Config**
   ```python
   EMAIL = "your-email@gmail.com"
   PASSWORD = "xxxx xxxx xxxx xxxx"  # Your 16-character app password
   ```

### Email Features
- 📧 Formatted HTML emails with job details
- 🔗 Direct "Apply Now" links
- 📊 Job information: Title, Company, Location, Salary, Source
- 📦 Batch sending for large job lists

### Example Email Content
```
Job Title: Senior Python Developer
Company: Tech Corp Inc.
Location: San Francisco, CA
Salary: $120,000 - $160,000
Source: LinkedIn

[Apply Now Button]
```

---

## 📤 Output

### Excel File
- **Location:** `output/jobs_YYYYMMDD_HHMM.xlsx`
- **Features:**
  - Formatted headers (blue background, white text)
  - Auto-sized columns
  - All job details included
  - Ready for analysis

### CSV File
- **Location:** `output/jobs_YYYYMMDD_HHMM.csv`
- **Features:**
  - Standard CSV format
  - Compatible with any spreadsheet
  - Easy to import into databases

### Sample Data
| Title | Company | Location | Salary | Source | Date Scraped |
|-------|---------|----------|--------|--------|--------------|
| Senior Python Dev | Tech Corp | SF, CA | $150K | LinkedIn | 2026-03-08 |
| React Engineer | Startup XY | Remote | $130K | Wellfound | 2026-03-08 |

---

## 🔧 Advanced Configuration

### Custom Search Locations
```python
# In utils/config.py
LOCATION = "San Francisco"   # Change to your target location
```

### Email Batch Size
```python
JOBS_PER_EMAIL = 5  # Number of jobs per email
```

### Scraper Timeout
```python
TIMEOUT = 30  # Seconds to wait for response
MAX_RETRIES = 3  # Number of retry attempts
```

### Duplicate Detection Fields
```python
DUPLICATE_CHECK_FIELDS = ["title", "company", "location"]
```

---

## 🐛 Troubleshooting

### Email Not Sending
**Error:** `SMTPAuthenticationError: Username and Password not accepted`

**Solution:**
1. Use Gmail App Password (not regular password)
2. Enable 2-Factor Authentication
3. Verify `EMAIL` and `PASSWORD` in config.py
4. Check if "Less secure app access" is disabled (recommended)

### No Jobs Found
**Possible Causes:**
1. Website structure changed (selectors may be outdated)
2. Website blocked scraping (use VPN or residential proxies)
3. Network connectivity issues

**Solutions:**
1. Update selectors in specific scraper files
2. Check user-agent in config.py
3. Verify internet connection

### Low Filtered Results
**Possible Causes:**
1. Search skills too restrictive
2. Search queries not matching job market
3. Location filtering too narrow

**Solutions:**
1. Add more skills to `JOB_SKILLS` in config.py
2. Diversify `SEARCH_QUERIES`
3. Change `LOCATION` or remove location filter

### Scheduler Not Running
**Solution:**
```bash
# Make sure scheduler is enabled
ENABLE_SCHEDULER = True  # in config.py

# Run in background (Windows)
python main.py &

# Or use Windows Task Scheduler to run daily
```

---

## 📈 Performance Tips

1. **Optimize Search Queries** - Specific queries return better results
2. **Adjust Skill List** - Fewer skills = more results, but less relevant
3. **Increase Retry Attempts** - For unstable connections
4. **Schedule Off-Peak** - Run scraper during off-peak hours
5. **Use Filtering** - Filter by location to reduce results

---

## 🤝 Contributing

Contributions are welcome! To add support for a new job platform:

1. Create new scraper in `scrapers/new_platform_scraper.py`
2. Implement `NewPlatformScraper` class with `scrape()` method
3. Return list of dictionaries with keys: `title`, `company`, `location`, `salary`, `link`, `source`, `date_scraped`
4. Add to scraper list in `main.py`
5. Test thoroughly
6. Submit pull request

### Example Scraper Template
```python
class NewPlatformScraper:
    def scrape(self, query="software developer", location=""):
        jobs = []
        # Your scraping logic here
        return jobs
```

---

## ⚖️ Legal & Ethics

- ✅ Respects website `robots.txt` and Terms of Service
- ✅ Implements rate limiting and delays
- ✅ Uses proper User-Agent headers
- ✅ Not intended for commercial resale
- ✅ Personal/research use recommended

*Always check website Terms of Service before scraping.*

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🎯 Roadmap

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web dashboard for job browsing
- [ ] Advanced filtering (salary range, experience level)
- [ ] Custom notifications (Slack, Discord, Telegram)
- [ ] Resume matching based on job descriptions
- [ ] Mobile app for job alerts
- [ ] Machine learning for job relevance ranking

---

## 📞 Support

For issues, questions, or suggestions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review `utils/config.py` for configuration tips
3. Check selector accuracy in scraper files
4. Submit issue with error details

---

## 🌟 Acknowledgments

- Built with ❤️ using Python
- Inspired by best practices in web scraping
- Community feedback and contributions

---

**Last Updated:** March 8, 2026
**Version:** 2.0 (Production Ready)

#   A I - J o b - S c r a p e r 
 
 