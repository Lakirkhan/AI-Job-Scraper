# Configuration file for Job Scraper

# Email Configuration
EMAIL = "your-email@gmail.com"  # Replace with your Gmail
PASSWORD = "your-app-password"  # Use Gmail App Password, not regular password
RECIPIENT_EMAIL = "recipient@gmail.com"  # Email to receive job alerts

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