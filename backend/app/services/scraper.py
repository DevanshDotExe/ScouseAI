import requests
from bs4 import BeautifulSoup
from typing import List, Dict

# --- Helper function for Source 1: DuckDuckGo ---
def _scrape_duckduckgo(entity_name: str, headers: dict) -> List[Dict[str, str]]:
    """Scrapes DuckDuckGo and returns a list of articles with titles and URLs."""
    print("Scraping DuckDuckGo...")
    url = f"https://html.duckduckgo.com/html/?q={entity_name} news"
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='result__a')
    
    articles = []
    for link in results[:5]:
        title = link.get_text(strip=True)
        # DuckDuckGo URLs are relative, so we need to clean them up
        raw_url = link.get('href', '')
        # The actual URL is in a query parameter, so we extract it
        if raw_url and 'uddg=' in raw_url:
            clean_url = requests.utils.unquote(raw_url.split('uddg=')[1])
            articles.append({'title': title, 'url': clean_url})
    return articles

# --- Helper function for Source 2: Bing ---
def _scrape_bing(entity_name: str, headers: dict) -> List[Dict[str, str]]:
    """Scrapes Bing News and returns a list of articles with titles and URLs."""
    print("Scraping Bing News...")
    url = f"https://www.bing.com/news/search?q={entity_name}"
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select("a.title")

    articles = []
    for link in results[:5]:
        title = link.get_text(strip=True)
        url = link.get('href', '')
        if title and url:
            articles.append({'title': title, 'url': url})
    return articles

# --- Main orchestrator function ---
async def scrape_web(entity_name: str) -> List[Dict[str, str]]:
    """
    Orchestrates scraping from multiple sources and returns a de-duplicated list of articles.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_articles = []
    
    try:
        all_articles.extend(_scrape_duckduckgo(entity_name, headers))
    except Exception as e:
        print(f"Warning: Could not scrape DuckDuckGo. Reason: {e}")

    try:
        all_articles.extend(_scrape_bing(entity_name, headers))
    except Exception as e:
        print(f"Warning: Could not scrape Bing. Reason: {e}")

    # De-duplicate articles based on the URL
    unique_articles = list({article['url']: article for article in all_articles}.values())
        
    print(f"Successfully aggregated {len(unique_articles)} unique articles.")
    return unique_articles