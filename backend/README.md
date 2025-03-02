# JioPay RAG Chatbot Backend

This is the backend for the JioPay RAG Chatbot, a customer support chatbot that uses Retrieval-Augmented Generation (RAG) to provide accurate answers based on JioPay's documentation.

## Features

- **FastAPI Backend**: Modern, fast API framework with automatic OpenAPI documentation
- **RAG Architecture**: Combines retrieval-based and generation-based approaches for accurate answers
- **Vector Search**: Uses FAISS for efficient similarity search
- **Web Scraping**: Collects data from JioPay's website and help center
- **Chunking Strategy**: Processes documents into optimal chunks for retrieval
- **Advanced Universal Scraper**: Scrape any website with intelligent content extraction and convert it to a vector store

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Data Collection and Processing

### Option 1: Use the JioPay Scraper

1. Run the scraper to collect data from JioPay's website:
   ```bash
   python scripts/scraper.py
   ```

2. Process the data and create vector embeddings:
   ```bash
   python scripts/indexer.py
   ```

### Option 2: Use the Advanced Universal Scraper

The advanced universal scraper allows you to scrape any website with intelligent content extraction and convert it to a vector store for use with the RAG chatbot.

```bash
python scripts/universal_scraper.py <url> [options]
```

#### Arguments

- `url`: The URL of the website to scrape (required)

#### Options

- `--max-pages`: Maximum number of pages to scrape (default: 100)
- `--delay-min`: Minimum delay between requests in seconds (default: 1.0)
- `--delay-max`: Maximum delay between requests in seconds (default: 3.0)
- `--max-depth`: Maximum depth to crawl from the starting URL (default: 5)
- `--output-dir`: Directory to save the scraped data (default: `data/raw/<domain>`)
- `--no-robots`: Ignore robots.txt rules (default: false)
- `--timeout`: Request timeout in seconds (default: 15)

#### Example

```bash
# Scrape a website with default settings
python scripts/universal_scraper.py https://example.com

# Scrape a website with custom settings
python scripts/universal_scraper.py https://example.com --max-pages 100 --delay-min 2.0 --delay-max 5.0 --max-depth 3 --output-dir data/raw/example --no-robots
```

#### Advanced Features

- **Robots.txt Compliance**: Respects website crawling rules by default
- **Intelligent Content Extraction**: Identifies and extracts the main content area of each page
- **URL Normalization**: Removes fragments, default ports, and tracking parameters
- **Retry Logic**: Automatically retries failed requests with exponential backoff
- **Progress Tracking**: Shows a progress bar during scraping
- **Logging**: Detailed logging to both console and file
- **Error Handling**: Robust error handling for various failure scenarios
- **Content Type Filtering**: Skips non-HTML content
- **File Extension Filtering**: Skips files like PDFs, images, CSS, and JavaScript

### Option 3: Use Sample Data

Process the sample data included in the repository:

```bash
python scripts/process_sample_data.py
```

## Running the API

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `POST /api/chat`: Process a chat request and return a response
- `GET /api/health`: Check the health of the API 