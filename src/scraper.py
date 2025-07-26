import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import json
from datetime import datetime
import config
from src.utils import setup_logging, safe_request_delay, ensure_data_directory

class WikipediaScraper:
    def __init__(self, use_selenium=False):
        self.logger = setup_logging()
        self.use_selenium = use_selenium
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if use_selenium:
            self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def get_random_articles(self, count=5):
        """Get random Wikipedia articles"""
        articles = []
        
        for i in range(count):
            try:
                # Get random article URL
                random_url = f"{config.WIKIPEDIA_BASE_URL}/wiki/Special:Random"
                
                if self.use_selenium:
                    self.driver.get(random_url)
                    current_url = self.driver.current_url
                    page_source = self.driver.page_source
                else:
                    response = self.session.get(random_url)
                    current_url = response.url
                    page_source = response.text
                
                # Parse the article
                article_data = self.parse_article(page_source, current_url)
                if article_data:
                    articles.append(article_data)
                    self.logger.info(f"Scraped article: {article_data['title']}")
                
                safe_request_delay(config.DELAY_BETWEEN_REQUESTS)
                
            except Exception as e:
                self.logger.error(f"Error scraping article {i+1}: {str(e)}")
                continue
        
        return articles
    
    def parse_article(self, html_content, url):
        """Parse Wikipedia article content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        try:
            # Extract basic information
            title = soup.find('h1', {'id': 'firstHeading'}).get_text().strip()
            
            # Extract first paragraph
            content_div = soup.find('div', {'id': 'mw-content-text'})
            paragraphs = content_div.find_all('p')
            first_paragraph = ""
            
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50 and not text.startswith('Coordinates:'):
                    first_paragraph = text
                    break
            
            # Extract infobox data if available
            infobox = {}
            infobox_table = soup.find('table', {'class': 'infobox'})
            if infobox_table:
                rows = infobox_table.find_all('tr')
                for row in rows:
                    header = row.find('th')
                    data = row.find('td')
                    if header and data:
                        key = header.get_text().strip()
                        value = data.get_text().strip()
                        infobox[key] = value
            
            # Extract categories
            categories = []
            category_links = soup.find_all('a', href=lambda x: x and '/wiki/Category:' in x)
            for link in category_links[:5]:  # Limit to first 5 categories
                categories.append(link.get_text().strip())
            
            return {
                'title': title,
                'url': url,
                'first_paragraph': first_paragraph[:500],  # Limit length
                'infobox': infobox,
                'categories': categories,
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(first_paragraph.split())
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing article: {str(e)}")
            return None
    
    def save_to_csv(self, articles, filename=None):
        """Save articles to CSV file"""
        ensure_data_directory()
        
        if not filename:
            filename = f"data/wikipedia_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'url', 'first_paragraph', 'categories', 'word_count', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for article in articles:
                # Convert lists to strings for CSV
                row = article.copy()
                row['categories'] = ', '.join(article['categories'])
                row['infobox'] = json.dumps(article['infobox'])
                writer.writerow({k: v for k, v in row.items() if k in fieldnames})
        
        self.logger.info(f"Saved {len(articles)} articles to {filename}")
        return filename
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    """Main scraping function"""
    scraper = WikipediaScraper(use_selenium=False)
    
    try:
        # Scrape articles
        articles = scraper.get_random_articles(config.MAX_ARTICLES)
        
        if articles:
            # Save to CSV
            csv_file = scraper.save_to_csv(articles)
            
            # Return results for email notification
            return {
                'success': True,
                'articles_count': len(articles),
                'csv_file': csv_file,
                'articles': articles
            }
        else:
            return {
                'success': False,
                'error': 'No articles were scraped'
            }
    
    finally:
        scraper.close()

if __name__ == "__main__":
    result = main()
    print(f"Scraping completed: {result}")
