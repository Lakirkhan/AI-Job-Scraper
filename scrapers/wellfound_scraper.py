"""
Wellfound (AngelList) Job Scraper
Scrapes job listings from Wellfound.com (formerly AngelList)
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class WellfoundScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://wellfound.com/jobs"
        self.jobs = []
    
    def scrape(self, query="software engineer", location=""):
        """
        Scrape Wellfound for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            url = f"{self.base_url}?query={query.replace(' ', '%20')}"
            
            for attempt in range(MAX_RETRIES):
                try:
                    response = self.session.get(url, timeout=TIMEOUT)
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        raise
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Wellfound job card selectors
            job_cards = soup.find_all('div', class_='job-card')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            print(f"✓ Wellfound: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ Wellfound scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('h2', class_='job-title')
            title_text = title.text.strip() if title else None
            
            company = card.find('p', class_='company-name')
            company_text = company.text.strip() if company else None
            
            location = card.find('p', class_='job-location')
            location_text = location.text.strip() if location else None
            
            link = card.find('a', class_='job-link')
            link = link.get('href') if link else None
            if link and not link.startswith('http'):
                link = f"https://wellfound.com{link}"
            
            if not all([title_text, company_text, location_text, link]):
                return None
            
            return {
                'title': title_text,
                'company': company_text,
                'location': location_text,
                'salary': 'Not available',
                'link': link,
                'source': 'Wellfound',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None
