import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

class SpoonacularScraper:
    def __init__(self):
        self.base_url = "https://spoonacular.com/food-api/docs"
        self.docs_dir = "spoonacular_docs"
        
        # Create docs directory if it doesn't exist
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)

    def get_soup(self, url):
        """Get BeautifulSoup object for a given URL."""
        try:
            print(f"Fetching: {url}")
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html5lib')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def extract_parameters(self, section):
        """Extract parameters from the documentation section."""
        parameters = {}
        
        # Find the Parameters section
        params_header = None
        for h4 in section.find_all('h4'):
            if h4.text.strip() == 'Parameters':
                params_header = h4
                break
        
        if not params_header:
            return parameters
            
        # Find the table after the Parameters header
        params_table = params_header.find_next('table')
        if not params_table:
            return parameters
            
        # Extract headers
        headers = [th.text.strip() for th in params_table.find_all('th')]
        if not headers:
            return parameters
            
        # Extract rows
        rows = params_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= len(headers):
                param_data = {}
                for i, col in enumerate(cols):
                    param_data[headers[i]] = col.text.strip()
                if 'Name' in param_data:
                    parameters[param_data['Name']] = param_data
                    
        return parameters

    def extract_endpoint_info(self, section):
        """Extract endpoint information from a documentation section."""
        # Get the title from the section attributes or h2
        title = section.get('jss-title', '')
        if not title:
            h2 = section.find('h2')
            title = h2.text.strip() if h2 else "Untitled"

        # Get the group from section attributes
        group = section.get('jss-group', 'Other')

        # Get the description from the first paragraph
        description = section.find('p')
        description_text = description.text.strip() if description else ""

        # Extract endpoint URL and method
        endpoint_url = ""
        endpoint_method = ""
        api_path_line = section.find('div', {'class': 'api-path-line'})
        if api_path_line:
            method_div = api_path_line.find('div', {'class': 'api-method'})
            endpoint_method = method_div.text.strip() if method_div else ""
            
            path_div = api_path_line.find('div', {'class': 'api-path'})
            endpoint_url = path_div.text.strip() if path_div else ""

        # Extract parameters
        parameters = self.extract_parameters(section)

        # Extract code examples
        code_examples = []
        for pre in section.find_all('pre'):
            code = pre.find('code')
            if code:
                code_examples.append({
                    'language': code.get('class', [''])[0].replace('language-', ''),
                    'code': code.text.strip()
                })
            else:
                code_examples.append({
                    'language': 'text',
                    'code': pre.text.strip()
                })

        # Extract quota information
        quota_text = ""
        quota_div = section.find('div', {'class': 'divText'})
        if quota_div:
            quota_text = quota_div.text.strip()

        return {
            'title': title,
            'group': group,
            'description': description_text,
            'endpoint_url': endpoint_url,
            'endpoint_method': endpoint_method,
            'parameters': parameters,
            'code_examples': code_examples,
            'quota': quota_text
        }

    def save_endpoint_info(self, endpoint_info):
        """Save endpoint information to a JSON file."""
        if not endpoint_info or not endpoint_info['title']:
            return

        # Create a filename from the title
        filename = re.sub(r'[^a-zA-Z0-9]+', '-', endpoint_info['title']).strip('-').lower()
        if not filename:
            return
        filename = f"{filename}.json"
        
        filepath = os.path.join(self.docs_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(endpoint_info, f, indent=2, ensure_ascii=False)
        print(f"Saved content to {filepath}")

    def scrape(self):
        """Main scraping function."""
        print("Starting scrape of Spoonacular API documentation...")
        
        # Get the main page
        soup = self.get_soup(self.base_url)
        if not soup:
            print("Failed to fetch main page")
            return

        # Find all documentation sections
        sections = soup.find_all('section', {'class': 'jss-doc'})
        if not sections:
            print("Could not find documentation sections")
            return

        # Process each section
        for section in sections:
            endpoint_info = self.extract_endpoint_info(section)
            if endpoint_info:
                self.save_endpoint_info(endpoint_info)

        print(f"Scraping completed. Processed {len(sections)} sections.")

if __name__ == "__main__":
    scraper = SpoonacularScraper()
    scraper.scrape()