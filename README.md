# API Documentation Scraper

A modern, user-friendly web interface for scraping and displaying API documentation. This tool allows you to paste any API documentation URL and get a clean, organized view of its endpoints.

## Features

- Modern dark theme interface
- Real-time endpoint search
- Beautiful card-based layout
- Parameter and code example display
- Responsive design
- Easy to use interface

## Setup

1. Clone the repository:
```bash
git clone https://github.com/sirakinb/spoonaculardocscraper.git
cd spoonaculardocscraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the URL of the API documentation page in the input field
2. Click "Scrape Documentation"
3. Wait for the scraper to process the documentation
4. Use the search bar to filter endpoints
5. Click on any endpoint card to view detailed information

## Project Structure

```
spoonaculardocscraper/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Styles for the web interface
│   └── js/
│       └── main.js    # Frontend JavaScript
└── templates/
    └── index.html     # Main HTML template
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 