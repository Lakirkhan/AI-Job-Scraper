# 🚀 AI Job Scraper

An automated **Python-based job scraping system** that collects software
development jobs from multiple platforms and exports them into Excel
while sending job alerts via email.

This project is designed for developers searching for roles in:

-   React.js
-   Node.js
-   Python
-   Laravel
-   PHP
-   AI / ML
-   Full Stack Development

The scraper gathers job listings based on **skills and location**,
stores them in **Excel**, and optionally sends **email notifications**.

------------------------------------------------------------------------

# ✨ Features

✅ Scrapes jobs from multiple platforms\
- LinkedIn\
- Naukri\
- Indeed

✅ Skill-based job filtering\
- React.js\
- Node.js\
- Python\
- Laravel\
- PHP\
- AI / ML

✅ Location-based search

✅ Automatic Excel export

✅ Email notifications with job details

✅ Centralized and clean project structure

✅ Ready to upload to GitHub

------------------------------------------------------------------------

# 📂 Project Structure

    AI-Job-Scraper
    │
    ├── main.py
    ├── config.py
    ├── requirements.txt
    │
    ├── scrapers
    │   ├── linkedin_scraper.py
    │   ├── naukri_scraper.py
    │   └── indeed_scraper.py
    │
    ├── utils
    │   ├── excel_exporter.py
    │   └── email_sender.py
    │
    └── output
        └── jobs.xlsx

------------------------------------------------------------------------

# ⚙️ Installation

Clone the repository

    git clone https://github.com/yourusername/AI-Job-Scraper.git
    cd AI-Job-Scraper

Create virtual environment

    python -m venv venv

Activate virtual environment

### Windows

    venv\Scripts\activate

### Mac / Linux

    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

# ▶️ Running the Scraper

Run the main script

    python main.py

Output:

-   Excel file generated inside `output/`
-   Email notification sent with job listings

Example:

    output/jobs_2026.xlsx

------------------------------------------------------------------------

# 📧 Email Configuration

Edit **config.py**

    EMAIL = "your_email@gmail.com"
    PASSWORD = "your_app_password"
    RECEIVER = "your_email@gmail.com"

⚠️ Use **Google App Password**, not your Gmail password.

Guide: https://support.google.com/accounts/answer/185833

------------------------------------------------------------------------

# 📊 Excel Output Format

  Title              Company    Location   Skills           Link
  ------------------ ---------- ---------- ---------------- ------------
  Python Developer   ABC Tech   Remote     Python, Django   Apply Link

------------------------------------------------------------------------

# 🔧 Future Improvements

-   Add more job sites
-   Telegram job alerts
-   Web dashboard
-   Job deduplication
-   Docker support

------------------------------------------------------------------------

# 🤝 Contributing

Pull requests are welcome.

If you find a bug or want to improve the scraper, feel free to
contribute.

------------------------------------------------------------------------

# ⭐ Support

If you like this project:

⭐ Star the repository\
🍴 Fork it\
📢 Share it with developers

------------------------------------------------------------------------

# 📜 License

MIT License