import os
import time
import random
import logging
from bs4 import BeautifulSoup 
from playwright.sync_api import sync_playwright

# --- 1. Global Configuration and Anti-Blocking Lists ---

# Indeed search URL components (fetched from Render Environment Variables)
JOB_TITLE = os.getenv("JOB_TITLE", "Software Engineer")
JOB_LOCATION = os.getenv("JOB_LOCATION", "Remote")
INDEED_BASE_URL = "https://www.indeed.com/jobs"

# List of realistic User-Agents to rotate (add more for better evasion)
USER_AGENTS = [ 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
]

# --- 2. Helper Functions ---

def implement_delay():
    """Pauses execution for a random period (5-15 seconds)."""
    pause_time = random.randint(5, 15)
    logging.info(f"--- Pausing for {pause_time} seconds to avoid rate limiting. ---")
    time.sleep(pause_time)

# --- 3. Core Scraping Function (Playwright) ---

def scrape_indeed(url):
    """Launches Playwright, navigates to Indeed, and returns the rendered HTML."""
    try:
        with sync_playwright() as p:
            # Launch the browser with a random User-Agent
            user_agent = random.choice(USER_AGENTS)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=user_agent)
            page = context.new_page()

            logging.info(f"Navigating with User-Agent: {user_agent}")
            page.goto(url, timeout=60000)

            # Wait for the job listings element to appear (JS content loaded)
            JOB_CARD_SELECTOR = 'div.jobsearch-SerpJobCard' # Check this selector if Indeed changes
            page.wait_for_selector(JOB_CARD_SELECTOR, timeout=15000) 
            
            html_content = page.content()
            browser.close()
            return html_content
    except Exception as e:
        logging.error(f"Playwright/Scraping Error: {e}")
        return None

# --- 4. Main Execution Logic ---

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Job Crawler Bot Started.")
    
    # 1. Build the initial search URL
    search_query = f"q={JOB_TITLE}&l={JOB_LOCATION}"
    
    # Simple loop for the first 3 pages (adjust range as needed)
    for page_number in range(3): 
        start_index = page_number * 10 # Indeed pagination uses 'start=0', 'start=10', etc.
        current_url = f"{INDEED_BASE_URL}?{search_query}&start={start_index}"
        
        logging.info(f"Scraping Page {page_number + 1} at: {current_url}")
        
        raw_html = scrape_indeed(current_url)
        
        if raw_html:
            # 2. Parse the HTML content
            soup = BeautifulSoup(raw_html, 'html.parser')
            
            # --- REPLACE THIS WITH YOUR ACTUAL PARSING LOGIC ---
            job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard') 
            logging.info(f"Found {len(job_cards)} job cards on Page {page_number + 1}.")
            # --- END PARSING LOGIC ---
            
            # 3. Process the data (save to database or send email)
            # You would call your database/email functions here
            
        else:
            logging.error(f"Failed to retrieve content for Page {page_number + 1}. Likely blocked.")
            break # Stop if we are blocked

        # 4. Anti-blocking delay before next page
        if page_number < 2: # Don't delay after the last page
            implement_delay() 

    logging.info("Job Crawler Bot Finished its run.")

if __name__ == "__main__":
    main()
