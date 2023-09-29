import spacy
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Tuple, Set

# Disable insecure request warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt',
                   '.pptx', '.zip', '.rar', '.jpg', '.jpeg', '.png', '.gif', '.rar']

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

    if link_parsed.netloc == base_url_parsed.netloc:
        return True

    if link.startswith("/") and not any(link.endswith(ext) for ext in FILE_EXTENSIONS):
        return True

    return False


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

    page_urls = {urljoin(base_url, link.get('href'))
                 for link in links if is_internal_link(base_url, link.get('href'))}
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

    for paragraph in soup.find_all('p'):
        cleaned_paragraph = clean_text(paragraph.get_text()).split('\n')
        for paragraph in cleaned_paragraph:
            if paragraph:
                page_paragraphs.append(paragraph)

    return page_paragraphs



def extract_metadata(url: str) -> Dict[str, Optional[str]]:
    """
    Extracts metadata information from the given URL.

    Args:
        url (str): The URL to extract metadata from.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing the extracted metadata.
    """
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata information
        metadata = {
            'title': soup.title.string.strip() if soup.title else None,
            'description': soup.find('meta', attrs={'name': 'description'})['content'].strip() if soup.find('meta', attrs={'name': 'description'}) else None,
            'keywords': soup.find('meta', attrs={'name': 'keywords'})['content'].strip() if soup.find('meta', attrs={'name': 'keywords'}) else None,
            # Add more metadata fields as needed
        }
        return metadata
    except (requests.RequestException, KeyError):
        return {}


# if __name__ == "__main__":
#     # Example usage
#     site_url = "https://stackoverflow.com/"
#     metadata = extract_metadata(site_url)
#     print("Title:", metadata.get('title'))
#     print("Description:", metadata.get('description'))
#     print("Keywords:", metadata.get('keywords'))
