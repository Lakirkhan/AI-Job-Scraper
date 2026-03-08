"""
Indeed Job Scraper
Scrapes job listings from Indeed.com
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class IndeedScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.indeed.com/jobs"
        self.jobs = []
    
    def scrape(self, query="software developer", location="Remote"):
        """
        Scrape Indeed for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            url = f"{self.base_url}?q={query}&l={location}&limit=50"
            
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
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception as e:
                    continue
            
            print(f"✓ Indeed: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ Indeed scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('h2', class_='jobTitle')
            title = title.text.strip() if title else None
            
            company = card.find('span', class_='company_location')
            company = company.text.strip() if company else None
            
            location = card.find('div', class_='company_location')
            location_elem = location.find_all('div')
            location = location_elem[-1].text.strip() if location_elem else None
            
            salary = card.find('span', class_='salary-snippet')
            salary = salary.text.strip() if salary else "Not available"
            
            link_elem = card.find('a', {'data-jk': True})
            link = f"https://indeed.com/viewjob?jk={link_elem['data-jk']}" if link_elem else None
            
            if not all([title, company, location, link]):
                return None
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'link': link,
                'source': 'Indeed',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None