"""
LinkedIn Job Scraper
Scrapes job listings from LinkedIn.com
Note: LinkedIn has anti-scraping measures. Use with caution.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from utils.config import USER_AGENT, TIMEOUT, MAX_RETRIES

class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.linkedin.com/'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.jobs = []
    
    def scrape(self, query="software developer", location="India"):
        """
        Scrape LinkedIn for jobs
        
        Args:
            query (str): Job search query
            location (str): Location filter
            
        Returns:
            list: List of job dictionaries
        """
        self.jobs = []
        
        try:
            # LinkedIn requires authentication, so direct scraping may be limited
            # This implementation attempts basic scraping
            url = f"{self.base_url}/?keywords={query}&location={location}"
            
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
                        print(f"⚠ LinkedIn: Requires authentication or has rate-limited access")
                        return self.jobs
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Job cards have various possible class names
            job_cards = soup.find_all('div', class_='base-card') or \
                       soup.find_all('li', class_='jobs-search__results-list-item')
            
            for card in job_cards[:50]:
                try:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                except Exception:
                    continue
            
            if self.jobs:
                print(f"✓ LinkedIn: Scraped {len(self.jobs)} jobs")
            else:
                print(f"⚠ LinkedIn: Limited access (authentication required)")
            
        except Exception as e:
            print(f"⚠ LinkedIn scraper: Limited access (authentication required)")
        
        time.sleep(2)
        return self.jobs
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            title = card.find('h3', class_='base-search-card__title')
            title = title.text.strip() if title else None
            
            company = card.find('h4', class_='base-search-card__subtitle')
            company = company.text.strip() if company else None
            
            location = card.find('span', class_='job-search-card__location')
            location = location.text.strip() if location else None
            
            link = card.find('a', class_='base-card__full-link')
            link = link.get('href', '').split('?')[0] if link else None
            
            if not all([title, company, location, link]):
                return None
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': 'Not available',
                'link': link,
                'source': 'LinkedIn',
                'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return None