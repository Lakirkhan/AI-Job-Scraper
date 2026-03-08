"""
Internshala Job Scraper
Scrapes job listings from Internshala.com (internships and entry-level jobs)
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class InternshalaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://internshala.com/jobs"
        self.jobs = []
    
    def scrape(self, query="python", location=""):
        """
        Scrape Internshala for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
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
            
            # Internshala job card selectors
            job_cards = soup.find_all('div', class_='job_card')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            print(f"✓ Internshala: Scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            print(f"✗ Internshala scraper error: {str(e)}")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('h3', class_='job_title')
            title_text = title.text.strip() if title else None
            
            company = card.find('h4', class_='company_name')
            company_text = company.text.strip() if company else None
            
            location = card.find('p', class_='location')
            location_text = location.text.strip() if location else None
            
            link = card.find('a')
            link = link.get('href') if link else None
            if link and not link.startswith('http'):
                link = f"https://internshala.com{link}"
            
            if not all([title_text, company_text, location_text, link]):
                return None
            
            return {
                'title': title_text,
                'company': company_text,
                'location': location_text,
                'salary': 'Not available',
                'link': link,
                'source': 'Internshala',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None
