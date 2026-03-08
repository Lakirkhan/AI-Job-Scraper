"""
Google Search Scraper
Searches Google for job listings and extracts URLs
"""

import requests
from bs4 import BeautifulSoup
import time
from utils.config import USER_AGENT, TIMEOUT

class GoogleSearchScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_jobs(self, query, num_results=5):
        """
        Search Google for job listings
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            list: List of URLs found
        """
        urls = []
        try:
            # Using DuckDuckGo as an alternative (Google blocking direct requests)
            search_url = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"
            
            response = self.session.get(search_url, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract URLs from search results
            for link in soup.find_all('a', href=True):
                if len(urls) >= num_results:
                    break
                    
                href = link.get('href')
                
                # Filter valid job site URLs
                if href and isinstance(href, str) and href.startswith('http'):
                    domain = href.split('/')[2].lower()
                    
                    # Check if it's a job site
                    if any(site in domain for site in ['linkedin', 'naukri', 'indeed', 
                                                        'glassdoor', 'wellfound', 'monster',
                                                        'timesjobs', 'internshala', 'foundit']):
                        urls.append(href)
            
            print(f"✓ Found {len(urls)} URLs for query: {query}")
            
        except Exception as e:
            print(f"✗ Error searching Google for '{query}': {str(e)}")
        
        time.sleep(2)  # Be respectful to servers
        return urls
    
    def search_multiple(self, queries):
        """
        Search multiple queries and return all URLs
        
        Args:
            queries (list): List of search queries
            
        Returns:
            list: Combined list of all URLs
        """
        all_urls = []
        
        for query in queries:
            print(f"Searching Google for: {query}")
            urls = self.search_jobs(query)
            all_urls.extend(urls)
            time.sleep(1)
        
        # Remove duplicates
        all_urls = list(set(all_urls))
        return all_urls
