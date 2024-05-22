
import requests
from bs4 import BeautifulSoup
import json
import os

SEARCH_ENGINE_ENDPOINT = os.getenv("SEARCH_ENGINE_ENDPOINT")
SEARCH_ENGINE_AUTH_KEY = os.getenv("SEARCH_ENGINE_AUTH_KEY")

def online_search(self, query: str) -> list[dict]:
    """
    Retrieve relevant contents online
  
    This function generates a list of dict, each one contains url, content.
    Args:
        query (str): String to search for.
    Returns:
        list([dict]): a list of result
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
        return [{"url": d["url"], "content": d["content"]} for d in results[:5]]

# def get_url_content(self, url: str) -> str:
#     """
#     Fetches HTML data from the given URL, parses it using BeautifulSoup, and extracts text content.

#     Args:
#         url (str): The URL to fetch data from.

#     Returns:
#         str: A JSON string containing either the extracted text or an error message.

#     Example:
#         url = "https://example.com"
#         result = get_url_content(url)
#         print(result)
#     """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for HTTP errors

#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Extract text from the parsed HTML
#         text_content = soup.get_text(separator="\n", strip=True)

#         # Return the extracted text content in a dictionary
#         return json.dumps({"content": text_content})
#     except requests.exceptions.RequestException as e:
#         # Handle any request-related errors
#         return json.dumps({"error": f"Request error: {str(e)}"})
#     except Exception as e:
#         # Handle any other parsing-related errors
#         return json.dumps({"error": f"Parsing error: {str(e)}"})


def get_url_content(self, urls: list[str]) -> str:
    """
    Attempts to fetch HTML data from a list of URLs, parses it using BeautifulSoup, and extracts text content.
    Moves to the next URL in the list if the current one fails.

    Args:
        urls (list): The list of URLs to fetch data from.

    Returns:
        str: A JSON string containing either the extracted text or an error message.

    Example:
        urls = ["https://example.com", "https://example2.com"]
        result = get_url_content(urls)
        print(result)
    """
    for url in urls:
        try:
            print(f"get_url_content: {url}")
            response = requests.get(url, timeout=100)  # Adding a timeout for the request
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract text from the parsed HTML
            text_content = soup.get_text(separator="\n", strip=True)

            # Return the first successful text content extraction
            return json.dumps({"content": text_content, "url": url})
        except requests.exceptions.RequestException as e:
            # Log the error and continue with the next URL
            continue  # Log the specific error and URL if necessary

    # Return error if all URLs fail
    return json.dumps({"error": "All URLs failed to provide valid content."})