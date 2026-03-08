"""
Foundit Job Scraper
Scrapes job listings from Foundit.in (formerly BaBajob, popular in India)
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class FounditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.foundit.in/jobs"
        self.jobs = []
    
    def scrape(self, query="software engineer", location=""):
        """
        Scrape Foundit for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            params = {
                'q': query,
                'l': location or ''
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
            
            # Foundit job card selectors
            job_cards = soup.find_all('div', class_='jobCard')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            print(f"✓ Foundit: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ Foundit scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('a', class_='jobTitle')
            title_text = title.text.strip() if title else None
            
            company = card.find('a', class_='companyName')
            company_text = company.text.strip() if company else None
            
            location = card.find('span', class_='jobLocation')
            location_text = location.text.strip() if location else None
            
            link = title.get('href') if title else None
            if link and not link.startswith('http'):
                link = f"https://www.foundit.in{link}"
            
            salary = card.find('span', class_='sal')
            salary_text = salary.text.strip() if salary else "Not available"
            
            if not all([title_text, company_text, location_text, link]):
                return None
            
            return {
                'title': title_text,
                'company': company_text,
                'location': location_text,
                'salary': salary_text,
                'link': link,
                'source': 'Foundit',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None
