import os
import time
import random
import logging
import requests # <-- Switch back to requests
from bs4 import BeautifulSoup 
# --- 1. Global Configuration and Anti-Blocking Lists ---
# --- 1. Global Configuration ---
# Fetch your API Key
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")

# Indeed search URL components (fetched from Render Environment Variables)
JOB_TITLE = os.getenv("JOB_TITLE", "Software Engineer")
JOB_LOCATION = os.getenv("JOB_LOCATION", "Remote")
# ... other variables ...
# Indeed search URL components (fetched from Render Environment Variables)
JOB_TITLE = os.getenv("JOB_TITLE", "Software Engineer")
JOB_LOCATION = os.getenv("JOB_LOCATION", "Remote")

# --- 2. Helper Functions ---

def implement_delay():
    """Pauses execution for a random period (5-15 seconds)."""
    pause_time = random.randint(5, 15)
    logging.info(f"--- Pausing for {pause_time} seconds to avoid rate limiting. ---")
    time.sleep(pause_time)

# --- 3. Core Scraping Function (Playwright) ---

# --- 3. Core Scraping Function (ScraperAPI) ---

def scrape_indeed(indeed_url):
    """
    Sends the Indeed URL to ScraperAPI for automated scraping.
    Uses 'render=True' to ensure JavaScript is executed.
    """
    if not SCRAPERAPI_KEY:
        logging.error("SCRAPERAPI_KEY environment variable is missing.")
        return None

    api_url = 'http://api.scraperapi.com/'
    
    # Parameters for ScraperAPI
    payload = {
        'api_key': SCRAPERAPI_KEY,
        'url': indeed_url,
        # IMPORTANT: Use render=True to execute JavaScript (needed for Indeed)
        'render': 'true', 
        'country_code': 'us' # Optional: Use this if targeting US jobs
    }
    
    try:
        logging.info(f"Sending request to ScraperAPI for: {indeed_url}")
        response = requests.get(api_url, params=payload, timeout=60) # Increased timeout
        
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"ScraperAPI failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"ScraperAPI Request Error: {e}")
        return None

# --- 4. Main Execution Logic ---

# --- 4. Main Execution Logic ---
def main():
    # ... setup and logging ...
    
    # Simple loop for the first 3 pages
    for page_number in range(3): 
        # ... setup URL ...
        
        # 1. Call the new ScraperAPI Function
        raw_html = scrape_indeed(current_url) # current_url is the Indeed URL
        
        if raw_html:
            # 2. Parse the HTML (now the HTML is guaranteed to be rendered)
            soup = BeautifulSoup(raw_html, 'html.parser')
            # ... continue parsing logic ...
        
        # 3. Keep the delay for courtesy (though less critical with an API)
        if page_number < 2: 
            implement_delay() 
    # ...
