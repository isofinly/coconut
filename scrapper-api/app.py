from flask import Flask, request, jsonify, Response
from typing import Any, Dict, List

from scrapper import extract_keywords_multilang, extract_metadata, extract_paragraphs, get_domain, get_site_pages, load_models

app = Flask(__name__)

# Load language models when the app starts
load_models()


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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
        data: Dict[str, Any] = request.json
        url: str = data.get('url', '')
        metadata: Dict[str, Any] = extract_metadata(url)
        return jsonify(metadata)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
