import spacy
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Tuple, Set
import concurrent.futures

import nltk
from nltk.corpus import wordnet
import numpy as np
import Levenshtein
from nltk.corpus.reader.wordnet import Synset

# Disable insecure request warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.jpg', '.jpeg', '.png', '.gif', '.rar']


MODELS: Dict[str, spacy.Language] = {}

def load_models() -> None:
    """
    Load models for different languages.

    :return: None
    """
    MODELS["ru"] = spacy.load("ru_core_news_sm")
    MODELS["en"] = spacy.load("en_core_web_sm")
    MODELS["uk"] = spacy.load("uk_core_news_sm")
    MODELS["ro"] = spacy.load("ro_core_news_sm")
    MODELS["fr"] = spacy.load("fr_core_news_sm")
    MODELS["de"] = spacy.load("de_core_news_sm")

def extract_keywords_multilang(text: str) -> Tuple[str, str, List[str]]:
    """
    Extract keywords from multilingual text.

    Args:
        text (str): The input text.

    Returns:
        Tuple[str, str, List[str]]: A tuple containing the detected language,
        the name of the NLP model used, and a list of keywords.
    """
    # Cache detected language
    detected_language = detect(text)
    nlp = MODELS.get(detected_language, MODELS["ru"])  # Default to Russian model
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "ADJ")]

    return detected_language, nlp.meta["name"], keywords


def get_domain(base_url: str) -> str:
    """
    Extracts the domain from a given URL.

    Args:
        base_url (str): The URL to extract the domain from.

    Returns:
        str: The domain extracted from the URL.
    """
    return urlparse(base_url).netloc


def is_internal_link(base_url: str, link: str) -> bool:
    """
    Check if a link is an internal link.

    Args:
        base_url (str): The base URL.
        link (str): The link to be checked.

    Returns:
        bool: True if the link is an internal link, False otherwise.
    """
    base_url_parsed = urlparse(base_url)
    link_parsed = urlparse(link)

    return link_parsed.netloc == base_url_parsed.netloc or (link.startswith("/") and not any(link.endswith(ext) for ext in FILE_EXTENSIONS))


def get_site_pages(url: str) -> Set[str]:
    """
    Retrieves all internal page URLs from a given website URL.

    Args:
        url (str): The URL of the website.

    Returns:
        Set[str]: A set of internal page URLs.
    """
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    base_url = response.url

    # Define a function to check if a link is internal and construct the full URL
    def process_link(link):
        if is_internal_link(base_url, link.get('href')):
            return urljoin(base_url, link.get('href'))

    # Use ThreadPoolExecutor to process links concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        page_urls = set(executor.map(process_link, links))

    return page_urls

def clean_text(text: str) -> str:
    """
    Cleans the given text by removing leading and trailing whitespace, newline characters, and tabs.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text with extra whitespace removed.
    """
    cleaned_text = text.strip().replace('\t', '')
    return ' '.join(cleaned_text.split())


def extract_paragraphs(url: str) -> List[str]:
    """
    Extracts paragraphs from the given URL.

    Args:
        url (str): The URL to extract paragraphs from.

    Returns:
        List[str]: A list of paragraphs extracted from the URL.
    """
    page_paragraphs = []

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        return page_paragraphs

    soup = BeautifulSoup(response.text, 'html.parser')

    # Define a function to extract and clean paragraphs
    def process_paragraph(paragraph):
        cleaned_paragraph = clean_text(paragraph.get_text()).split('\n')
        return [p for p in cleaned_paragraph if p]

    # Use ThreadPoolExecutor to process paragraphs concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        paragraphs_lists = list(executor.map(process_paragraph, soup.find_all('p')))

    # Flatten the list of lists into a single list of paragraphs
    page_paragraphs = [p for sublist in paragraphs_lists for p in sublist]

    return page_paragraphs


def extract_metadata(url: str) -> Dict[str, Optional[str]]:
    """
    Extracts metadata information from the given URL.

    Args:
        url (str): The URL to extract metadata from.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing the extracted metadata.
    """
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata information
    metadata = {
        'title': soup.title.string.strip() if soup.title else None,
        'description': soup.find('meta', attrs={'name': 'description'})['content'].strip() if soup.find('meta', attrs={'name': 'description'}) else None,
        'keywords': soup.find('meta', attrs={'name': 'keywords'})['content'].strip() if soup.find('meta', attrs={'name': 'keywords'}) else None,
        # Add more metadata fields as needed
        }
    
    if metadata['description'] and not metadata['keywords']:
        metadata['keywords'] = extract_keywords_multilang(metadata['description'])[2]
    return metadata


# TODO: Implement async, parallel processing and refine the function

def semantic_and_closest_match(array1: List[str], array2: List[str]) -> Tuple[str, str]:
    """
    Calculates the semantic and closest match between two arrays of strings.

    Args:
        array1 (List[str]): The first array of strings.
        array2 (List[str]): The second array of strings.

    Returns:
        Tuple[str, str, float]: A tuple containing the best match words from array1 and array2, 
        along with their combined score.
    """

    def semantic_similarity(word1: str, word2: str) -> float:
        synsets1: List[Synset] = wordnet.synsets(word1)
        synsets2: List[Synset] = wordnet.synsets(word2)

        max_similarity: float = 0.0

        for synset1 in synsets1:
            for synset2 in synsets2:
                similarity: float = synset1.wup_similarity(synset2)
                if similarity is not None and similarity > max_similarity:
                    max_similarity = similarity

        return max_similarity

    semantic_similarity_dict: dict = {}
    for word1 in array1:
        for word2 in array2:
            semantic_similarity_dict[(word1, word2)] = semantic_similarity(word1, word2)

    best_match: Tuple[str, str] = ("", "")
    best_score: float = -1

    for word1 in array1:
        for word2 in array2:
            semantic_score: float = semantic_similarity_dict[(word1, word2)]
            levenshtein_score: int = Levenshtein.distance(word1, word2)

            # You can adjust the weights for semantic and Levenshtein scores as needed
            combined_score: float = 0.7 * semantic_score + 0.3 * (1 / (1 + levenshtein_score))

            if combined_score > best_score:
                best_score = combined_score
                best_match = (word1, word2)

    return best_match[0], best_match[1]



# if __name__ == "__main__":
#     # Example usage
#     site_url = "https://stackoverflow.com/"
#     metadata = extract_metadata(site_url)
#     print("Title:", metadata.get('title'))
#     print("Description:", metadata.get('description'))
#     print("Keywords:", metadata.get('keywords'))