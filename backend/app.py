from flask import Flask, request, jsonify, Response
from typing import Any, Dict, List
import concurrent.futures

from scrapper import extract_keywords_multilang, extract_metadata, extract_paragraphs, get_domain, get_site_pages, load_models

app = Flask("scrapper-api")

# Load language models when the app starts
load_models()

@app.get('/')
def index() -> str:
    return 'Hello, World!'
@app.route('/extract_keywords', methods=['POST'])
def extract_keywords() -> Dict[str, Any]:
    """
    Extracts keywords from the given text and returns a dictionary 
    containing the detected language, model name, and keywords.

    Args:
        None

    Returns:
        A dictionary containing the detected language, model name, 
        and keywords.
    """
    data: Dict[str, Any] = request.json
    text: str = data.get('text', '')
    detected_language: str
    model_name: str
    keywords: List[str]

    detected_language, model_name, keywords = extract_keywords_multilang(
        text)

    result: Dict[str, Any] = {
        'detected_language': detected_language,
        'model_name': model_name,
        'keywords': keywords
    }
    return jsonify(result)


@app.route('/get_domain', methods=['POST'])
def get_domain_handler() -> str:
    """
    Handle the POST request to get the domain from the base URL.

    Args:
        None

    Returns:
        str: The domain extracted from the base URL.
    """
    data = request.json
    base_url: str = data.get('url', '')
    domain: str = get_domain(base_url)
    return jsonify({'domain': domain})


@app.route('/get_site_pages', methods=['POST'])
def get_site_pages_handler() -> jsonify:
    """
    Handler for the '/get_site_pages' route.
    Retrieves a list of page URLs for a given site URL.

    Args:
        None

    Returns:
        jsonify: A JSON response containing the list of page URLs.
    """
    data: dict = request.json
    site_url: str = data.get('url', '')
    page_urls: List[str] = list(get_site_pages(site_url))
    return jsonify({'page_urls': page_urls})


@app.route('/extract_paragraphs', methods=['POST'])
def extract_paragraphs_handler() -> Response:
    """
    Handler for extracting paragraphs from a given URL.

    Args:
        None

    Returns:
        Response: A JSON response containing the extracted paragraphs.
    """
    data: Dict[str, Any] = request.json
    url: str = data.get('url', '')
    paragraphs: List[str] = extract_paragraphs(url)
    return jsonify({'paragraphs': paragraphs})


@app.route('/extract_metadata', methods=['POST'])
def extract_metadata_handler() -> Dict[str, Any]:
    """
    Handle the POST request to extract metadata from a given URL.

    Args:
        None

    Returns:
        Dict[str, Any]: The extracted metadata.
    """
    data: Dict[str, Any] = request.json
    url: str = data.get('url', '')
    metadata: Dict[str, Any] = extract_metadata(url)
    return jsonify(metadata)

@app.route('/extract_metadata_batch', methods=['POST'])
def extract_metadata_batch_handler():
    if request.method == 'POST':
        data = request.json
        site_url = data.get('url', '')
        n = data.get('n', 5)  # Default to extracting metadata for 5 URLs
        page_urls = list(get_site_pages(site_url))[:n]

        metadata_list = []

        # Define a function to extract metadata for a single URL
        def extract_metadata_for_url(url):
            metadata = extract_metadata(url)
            return {'url': url, 'metadata': metadata}

        # Use ThreadPoolExecutor to execute the extraction concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks for each URL
            future_to_url = {executor.submit(extract_metadata_for_url, url): url for url in page_urls}

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    metadata_list.append(result)
                except Exception as e:
                    # Handle exceptions for individual URLs here
                    print(f"Error processing URL {url}: {str(e)}")

        return jsonify(metadata_list)
    

# TODO: Add a trend_finder handler, semantic_and_closest_match method from scrapper 

if __name__ == "__main__":
    app.run(port=3030, host='0.0.0.0')