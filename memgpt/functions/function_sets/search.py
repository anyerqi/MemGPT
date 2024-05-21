
import requests
from bs4 import BeautifulSoup
import json
import os

SEARCH_ENGINE_ENDPOINT = os.getenv("SEARCH_ENGINE_ENDPOINT")
SEARCH_ENGINE_AUTH_KEY = os.getenv("SEARCH_ENGINE_AUTH_KEY")

def online_search(self, query: str) -> list[str]:
    """
    Retrieve URLs of relevant contents online
  
    This function generates a list of URLs, which relevated to keyword user inputs, then use 'get_url_content' to get the content of the url.
    Args:
        query (str): String to search for.
    Returns:
        str: a list of URLs
    """
    
    url = f"{SEARCH_ENGINE_ENDPOINT}?q={query}&format=json"

    payload = {}
    headers = {
        'Authorization': f'Bearer {SEARCH_ENGINE_AUTH_KEY}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        return "something error"
    else:
        data = response.json()
        if "results" not in data or len(data["results"]) == 0:
            return f"No results found."
        results = data["results"]
        #results_pref = f"Showing {len(results)} results:"
        #results_formatted = [f"title: {d['title']}, content: {d['content']}, url: {d['url']}" for d in results]
        #results_str = f"{results_pref} {json.dumps(results_formatted, ensure_ascii=False)}"
        #return results_str
        return [d["url"] for d in results[:5]]

def get_url_content(self, url: str) -> str:
    """
    Fetches HTML data from the given URL, parses it using BeautifulSoup, and extracts text content.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        str: A JSON string containing either the extracted text or an error message.

    Example:
        url = "https://example.com"
        result = get_url_content(url)
        print(result)
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text from the parsed HTML
        text_content = soup.get_text(separator="\n", strip=True)

        # Return the extracted text content in a dictionary
        return json.dumps({"content": text_content})
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        return json.dumps({"error": f"Request error: {str(e)}"})
    except Exception as e:
        # Handle any other parsing-related errors
        return json.dumps({"error": f"Parsing error: {str(e)}"})
