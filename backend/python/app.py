from flask import Flask, request, jsonify, Response
from typing import Any, Dict, List
import concurrent.futures

import requests

from scrapper import extract_keywords_multilang, extract_metadata, extract_paragraphs, get_domain, get_site_pages, load_models
from trend_finder import get_interest_over_time, get_related_queries, get_related_topics

app = Flask("scrapper-api")

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load language models when the app starts
load_models()


@cross_origin()
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

# TODO: Make request to nodejs api if no response
# Make a similar handler in node
@cross_origin()
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

# TODO: Make request to nodejs api if no response
# Make a similar handler in node
@cross_origin()
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

# TODO: Make request to nodejs api if no response
# Make a similar handler in node
@cross_origin()
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

# TODO: Make request to nodejs api if no response
@cross_origin()
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

# TODO: Make request to nodejs api if no response
@cross_origin()
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
            future_to_url = {executor.submit(
                extract_metadata_for_url, url): url for url in page_urls}

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

@cross_origin()
@app.route('/get_interest_over_time', methods=['POST'])
def get_interest_over_time_route() -> Dict[str, Any]:
    """
    Handler for the '/get_interest_over_time' route.
    Expects a JSON payload with a 'query' field.
    Returns a JSON response with the 'interest_over_time' data.

    :return: A dictionary containing the 'interest_over_time' data.
    :rtype: dict
    """
    data: Dict[str, Any] = request.json
    query: List[str] = data.get('query', [])

    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400

    interest_over_time_data: List[dict[str, Any]] = get_interest_over_time(query)
    return jsonify({'interest_over_time': interest_over_time_data})

@cross_origin()
@app.route('/get_related_topics', methods=['POST'])
def get_related_topics_route() -> Dict[str, Any]:
    """
    Handle POST request to '/get_related_topics' endpoint.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing the related topics data.
    """
    data: Dict[str, Any] = request.json
    query: List[str] = data.get('query', [])

    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400

    related_topics_data: List[dict[str, Any]] = get_related_topics(query)
    return jsonify({'related_topics': related_topics_data})

@cross_origin()
@app.route('/get_related_queries', methods=['POST'])
def get_related_queries_route() -> Dict[str, List[str]]:
    """
    Retrieves related queries based on the given query.

    Args:
        query (List[str]): The query to retrieve related queries for.

    Returns:
        Dict[str, List[str]]: A dictionary containing the related queries.
    """
    data: Dict[str, List[str]] = request.json
    query: List[str] = data.get('query', [])

    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400

    related_queries_data: List[dict[str, Any]] = get_related_queries(query)
    return jsonify({'related_queries': related_queries_data})

def callNodejsAPI(url):
    response = requests.post("http://localhost:3050/extract_data", json={"url": [url]})
    return response

@cross_origin()
@app.route('/get_theme', methods=['POST'])
def get_theme():
    data = request.json
    

if __name__ == "__main__":
    app.run(port=3030, host='0.0.0.0')
