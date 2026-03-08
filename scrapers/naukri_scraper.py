"""
Naukri Job Scraper
Scrapes job listings from Naukri.com (popular in India)
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class NaukriScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.naukri.com"
        self.jobs = []
    
    def scrape(self, query="software", location="india"):
        """
        Scrape Naukri for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            # Naukri uses a specific URL pattern
            url = f"{self.base_url}/{query.replace(' ', '-')}-jobs"
            
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
            
            # Naukri uses article tags for job cards
            job_cards = soup.find_all('article', class_='jobTuple')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            print(f"✓ Naukri: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ Naukri scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            # Title
            title_elem = card.find('a', class_='jobTitle')
            title = title_elem.text.strip() if title_elem else None
            
            # Company
            company_elem = card.find('a', class_='subTitle')
            company = company_elem.text.strip() if company_elem else None
            
            # Location
            location_elem = card.find('li', class_='location')
            location = location_elem.text.strip() if location_elem else None
            
            # Link
            link = title_elem.get('href') if title_elem else None
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"
            
            # Salary
            salary_elem = card.find('li', class_='salary')
            salary = salary_elem.text.strip() if salary_elem else "Not available"
            
            if not all([title, company, location, link]):
                return None
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'link': link,
                'source': 'Naukri',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None