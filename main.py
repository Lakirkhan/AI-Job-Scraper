"""
Job Scraper Main Module
Orchestrates web scraping, filtering, and exporting of job listings
"""

import schedule
import time
from datetime import datetime

# Scrapers
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.naukri_scraper import NaukriScraper
from scrapers.indeed_scraper import IndeedScraper
from scrapers.glassdoor_scraper import GlassdoorScraper
from scrapers.wellfound_scraper import WellfoundScraper
from scrapers.monster_scraper import MonsterScraper
from scrapers.timesjobs_scraper import TimesjobsScraper
from scrapers.internshala_scraper import InternshalaScraper
from scrapers.foundit_scraper import FounditScraper

# Utilities
from filters.skill_filter import SkillFilter
from utils.email_sender import EmailSender
from utils.export_excel import ExcelExporter
from utils.csv_exporter import CSVExporter
from utils.deduplication import JobDeduploication
from utils.config import (
    JOB_SKILLS, LOCATION, ENABLE_SCHEDULER, SCHEDULE_TIME,
    SEND_EMAIL_ALERTS, SEARCH_QUERIES
)

class JobScraperSystem:
    def __init__(self):
        self.all_jobs = []
        self.filtered_jobs = []
        self.skill_filter = SkillFilter(JOB_SKILLS)
        self.email_sender = EmailSender()
        self.excel_exporter = ExcelExporter()
        self.csv_exporter = CSVExporter()
    
    def scrape_all_sources(self):
        """
        Scrape all job sources
        
        Returns:
            list: All scraped jobs from all sources
        """
        self.all_jobs = []
        
        print("\n" + "="*60)
        print(f"Starting Job Scraper - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        scrapers = [
            ("LinkedIn", LinkedInScraper()),
            ("Naukri", NaukriScraper()),
            ("Indeed", IndeedScraper()),
            ("Glassdoor", GlassdoorScraper()),
            ("Wellfound", WellfoundScraper()),
            ("Monster", MonsterScraper()),
            ("TimesJobs", TimesjobsScraper()),
            ("Internshala", InternshalaScraper()),
            ("Foundit", FounditScraper()),
        ]
        
        for name, scraper in scrapers:
            try:
                print(f"Scraping {name}...")
                jobs = scraper.scrape(location=LOCATION)
                self.all_jobs.extend(jobs)
            except Exception as e:
                print(f"✗ Error scraping {name}: {str(e)}")
        
        print(f"\n✓ Total Jobs Scraped: {len(self.all_jobs)}")
        return self.all_jobs
    
    def deduplicate_jobs(self):
        """Remove duplicate jobs"""
        print("\nRemoving duplicates...")
        self.all_jobs = JobDeduploication.remove_duplicates(self.all_jobs)
        print(f"✓ Jobs after deduplication: {len(self.all_jobs)}")
    
    def filter_jobs(self):
        """Filter jobs by required skills"""
        print("\nFiltering by required skills...")
        self.filtered_jobs = self.skill_filter.filter_jobs(self.all_jobs)
        print(f"✓ Filtered Jobs: {len(self.filtered_jobs)}")
    
    def export_jobs(self):
        """Export jobs to Excel and CSV"""
        if not self.filtered_jobs:
            print("\n⚠ No filtered jobs to export")
            return
        
        print("\nExporting jobs...")
        
        # Export to Excel
        excel_file = self.excel_exporter.export(self.filtered_jobs)
        
        # Export to CSV
        csv_file = self.csv_exporter.export(self.filtered_jobs)
        
        print(f"✓ Files exported successfully")
    
    def send_alerts(self):
        """Send email alerts"""
        if not self.filtered_jobs:
            print("\n⚠ No jobs to send in alert")
            return
        
        if not SEND_EMAIL_ALERTS:
            print("\n⚠ Email alerts disabled in config")
            return
        
        print("\nSending email alerts...")
        success = self.email_sender.send_email(self.filtered_jobs)
        
        if success:
            print(f"✓ Email alerts sent")
        else:
            print(f"✗ Failed to send email alerts")
    
    def run_once(self):
        """Run scraper once"""
        self.scrape_all_sources()
        self.deduplicate_jobs()
        self.filter_jobs()
        self.export_jobs()
        self.send_alerts()
        
        print("\n" + "="*60)
        print(f"Scraper Completed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
    
    def schedule_daily(self):
        """Schedule scraper to run daily"""
        if not ENABLE_SCHEDULER:
            print("Scheduler disabled. Running once...")
            self.run_once()
            return
        
        print(f"Scheduling scraper to run daily at {SCHEDULE_TIME}")
        schedule.every().day.at(SCHEDULE_TIME).do(self.run_once)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n✓ Scheduler stopped")

def main():
    """Main entry point"""
    scraper_system = JobScraperSystem()
    
    # Check if scheduler is enabled
    if ENABLE_SCHEDULER:
        scraper_system.schedule_daily()
    else:
        scraper_system.run_once()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Scraper interrupted by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()