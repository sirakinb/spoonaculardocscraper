from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

app = Flask(__name__)

class APIDocScraper:
    def __init__(self):
        self.endpoints = []
        self.base_url = None
        
    def scrape_documentation(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Store base URL for relative links
            self.base_url = '/'.join(url.split('/')[:3])
            
            # Find all endpoint sections
            # This is a generic approach - we'll need to adapt it based on the API docs structure
            sections = soup.find_all(['div', 'section'], class_=['endpoint', 'api-endpoint', 'method'])
            
            for section in sections:
                endpoint_info = self.extract_endpoint_info(section)
                if endpoint_info:
                    self.endpoints.append(endpoint_info)
            
            return {
                'success': True,
                'endpoints': self.endpoints,
                'total_endpoints': len(self.endpoints)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_endpoint_info(self, section):
        try:
            # Extract title
            title_elem = section.find(['h1', 'h2', 'h3', 'h4'])
            title = title_elem.text.strip() if title_elem else "Untitled Endpoint"
            
            # Extract description
            desc_elem = section.find(['p', 'div'], class_=['description', 'endpoint-description'])
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract endpoint URL
            url_elem = section.find(['code', 'pre'])
            endpoint_url = url_elem.text.strip() if url_elem else ""
            
            # Extract method
            method_elem = section.find(['span', 'div'], class_=['method', 'http-method'])
            method = method_elem.text.strip().upper() if method_elem else "GET"
            
            # Extract parameters
            params_table = section.find('table', class_=['parameters', 'params'])
            parameters = self.extract_parameters(params_table) if params_table else {}
            
            # Extract code examples
            code_examples = self.extract_code_examples(section)
            
            return {
                'title': title,
                'description': description,
                'endpoint_url': endpoint_url,
                'method': method,
                'parameters': parameters,
                'code_examples': code_examples
            }
            
        except Exception as e:
            print(f"Error extracting endpoint info: {str(e)}")
            return None
    
    def extract_parameters(self, table):
        params = {}
        if not table:
            return params
            
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 4:
                name = cols[0].text.strip()
                param_type = cols[1].text.strip()
                example = cols[2].text.strip()
                description = cols[3].text.strip()
                
                params[name] = {
                    'type': param_type,
                    'example': example,
                    'description': description
                }
        
        return params
    
    def extract_code_examples(self, section):
        examples = []
        code_blocks = section.find_all(['pre', 'code'], class_=['example', 'code-example'])
        
        for block in code_blocks:
            examples.append({
                'language': block.get('class', ['plaintext'])[0] if block.get('class') else 'plaintext',
                'code': block.text.strip()
            })
        
        return examples

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    scraper = APIDocScraper()
    result = scraper.scrape_documentation(url)
    
    if result['success']:
        # Save the results to a JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'api_docs_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 