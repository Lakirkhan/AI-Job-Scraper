"""
TimesJobs Job Scraper
Scrapes job listings from TimesJobs.com (popular in India)
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class TimesjobsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.timesjobs.com/candidate/job-search.html"
        self.jobs = []
    
    def scrape(self, query="software engineer", location="India"):
        """
        Scrape TimesJobs for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            params = {
                'searchType': 'personalizedSearch',
                'from': 'home',
                'txtKeywords': query,
                'txtLocation': location,
                'pageNum': 1
            }
            
            for attempt in range(MAX_RETRIES):
                try:
                    response = self.session.get(self.base_url, params=params, timeout=TIMEOUT)
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        raise
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # TimesJobs uses li with specific data attributes
            job_cards = soup.find_all('li', {'data-job-id': True})
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            print(f"✓ TimesJobs: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ TimesJobs scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('h2', class_='job-name')
            title_text = title.text.strip() if title else None
            
            company = card.find('h3', class_='job-company-name')
            company_text = company.text.strip() if company else None
            
            location = card.find('li', class_='job-location')
            location_text = location.text.strip() if location else None
            
            link = card.find('a')
            link = link.get('href') if link else None
            if link and not link.startswith('http'):
                link = f"https://www.timesjobs.com{link}"
            
            salary = card.find('li', class_='job-salary')
            salary_text = salary.text.strip() if salary else "Not available"
            
            if not all([title_text, company_text, location_text, link]):
                return None
            
            return {
                'title': title_text,
                'company': company_text,
                'location': location_text,
                'salary': salary_text,
                'link': link,
                'source': 'TimesJobs',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None
