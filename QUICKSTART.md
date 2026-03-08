# 🚀 Quick Start Guide

## 1️⃣ Initial Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure the System
```bash
python setup.py
```

This interactive script will ask you for:
- Gmail address & App Password (for email alerts)
- Target location for jobs
- Scheduler preference

### Step 3: Test Run
```bash
python main.py
```

---

## 📧 Email Setup (If You Want Alerts)

### Generate Gmail App Password:

1. Go to [Google Account Settings](https://myaccount.google.com/security)
2. Enable "2-Step Verification" (if not already done)
3. Find "App Passwords" in Security settings
4. Select "Mail" and "Windows Computer"
5. Google will generate 16-character password
6. Copy it to config during setup

**Why App Password?**
- Safer than regular password
- Works with Gmail's security
- Can be revoked anytime

---

## ⚡ Quick Usage

### Run Once (Single Execution)
```bash
python main.py
```

**Output:**
- `output/jobs_YYYYMMDD_HHMM.xlsx` - Excel file with filtered jobs
- `output/jobs_YYYYMMDD_HHMM.csv` - CSV file for import
- **Email** - If configured (with job alerts)

### Schedule Daily Runs
Edit `utils/config.py`:
```python
ENABLE_SCHEDULER = True
SCHEDULE_TIME = "09:00"  # 9 AM daily
```

Then run:
```bash
python main.py
```

---

## 🔧 Customize Skills Filter

Edit `utils/config.py` to change which technologies to filter:

```python
JOB_SKILLS = [
    "react",
    "python",
    "machine learning",
    # Add or remove skills as needed
]
```

---

## 📊 Check Results

### Excel Files
- Open `output/jobs_*.xlsx` in Excel/Google Sheets
- Formatted with colors, borders, auto-sized columns

### CSV Files
- Import into databases or other tools
- Standard CSV format

### Email
- Formatted HTML emails
- Direct "Apply Now" links
- One email per batch (default 5 jobs)

---

## 🆘 Troubleshooting

### No jobs found?
- Check internet connection
- Verify `LOCATION` in config.py
- Try different `SEARCH_QUERIES`
- Add more skills to filter

### Email not sending?
- Use Gmail App Password (not regular password)
- Enable 2-Step Verification
- Check EMAIL and PASSWORD in config.py
- See "Email Setup" section above

### Too many filtered jobs?
- Reduce number of skills in `JOB_SKILLS`
- Add more specific skills

### Too few jobs?
- Add more search queries
- Remove restrictive skills
- Change location

---

## 📚 Full Documentation

See README.md for:
- Detailed feature list
- All configuration options
- Advanced usage
- Contributing guide
- License information

---

## 🎯 Pro Tips

1. **Schedule with Windows Task Scheduler**
   - For always-running job scraper on Windows
   - Set up automatic daily runs

2. **Customize Search Queries**
   - Edit `SEARCH_QUERIES` in config for better results
   - Add location to queries: "Python developer jobs San Francisco"

3. **Filter by Salary**
   - Manually filter the Excel/CSV export
   - Or extend SkillFilter class for automatic filtering

4. **Track Over Time**
   - Save Excel files with dates
   - Compare job market trends

---

**Questions?** Check README.md or review config.py comments for more options!

