document.addEventListener('DOMContentLoaded', () => {
    const apiUrlInput = document.getElementById('apiUrl');
    const scrapeButton = document.getElementById('scrapeButton');
    const resultsSection = document.querySelector('.results-section');
    const endpointsGrid = document.querySelector('.endpoints-grid');
    const searchInput = document.getElementById('searchInput');
    const buttonText = scrapeButton.querySelector('.button-text');
    const loader = scrapeButton.querySelector('.loader');

    let endpoints = [];

    scrapeButton.addEventListener('click', async () => {
        const url = apiUrlInput.value.trim();
        if (!url) {
            showError('Please enter a valid URL');
            return;
        }

        try {
            setLoading(true);
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (data.success) {
                endpoints = data.endpoints;
                displayEndpoints(endpoints);
                resultsSection.style.display = 'block';
            } else {
                showError(data.error || 'Failed to scrape documentation');
            }
        } catch (error) {
            showError('An error occurred while scraping the documentation');
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    });

    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredEndpoints = endpoints.filter(endpoint => 
            endpoint.title.toLowerCase().includes(searchTerm) ||
            endpoint.description.toLowerCase().includes(searchTerm) ||
            endpoint.endpoint_url.toLowerCase().includes(searchTerm)
        );
        displayEndpoints(filteredEndpoints);
    });

    function displayEndpoints(endpoints) {
        endpointsGrid.innerHTML = endpoints.map(endpoint => `
            <div class="endpoint-card">
                <span class="endpoint-method method-${endpoint.method.toLowerCase()}">${endpoint.method}</span>
                <h3 class="endpoint-title">${endpoint.title}</h3>
                <div class="endpoint-url">${endpoint.endpoint_url}</div>
                <p class="endpoint-description">${endpoint.description}</p>
                
                ${Object.keys(endpoint.parameters).length > 0 ? `
                    <div class="parameters-section">
                        <h4 class="parameters-title">Parameters</h4>
                        ${Object.entries(endpoint.parameters).map(([name, param]) => `
                            <div class="parameter-item">
                                <span class="parameter-name">${name}</span>
                                <span class="parameter-type">${param.type}</span>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}

                ${endpoint.code_examples.length > 0 ? `
                    <div class="code-examples-section">
                        <h4 class="code-examples-title">Code Examples</h4>
                        ${endpoint.code_examples.map(example => `
                            <pre class="code-example"><code class="language-${example.language}">${example.code}</code></pre>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    function setLoading(isLoading) {
        scrapeButton.disabled = isLoading;
        buttonText.textContent = isLoading ? 'Scraping...' : 'Scrape Documentation';
        loader.style.display = isLoading ? 'block' : 'none';
    }

    function showError(message) {
        // You could implement a more sophisticated error display here
        alert(message);
    }
}); 