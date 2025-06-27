from src.config.logging import logger
from typing import Optional, List, Union
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from src.types.models import SearchResult
import json


class ReadWebPage:
    
    def __init__(self, user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', timeout: int = 10):
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_retries = 3
        self.headers = {
            'User-Agent': self.user_agent,
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Connection': 'keep-alive',
        }

    def get_and_format(self, url: str) -> SearchResult:
        # Default error result
        default_result = SearchResult(
            title=f"Unable to read content from {url}",
            query=url,
            summary=""
        )
        
        with requests.Session() as session:
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"Reading webpage: {url}")
                    
                    # Validate URL format
                    if not url.startswith(('http://', 'https://')):
                        logger.warning(f"Invalid URL format: {url}")
                        return SearchResult(
                            title="Invalid URL format",
                            query=url,
                            summary="URL must start with http:// or https://"
                        )
                    
                    # Get HTML source code of the webpage
                    response = session.get(url, headers=self.headers, timeout=self.timeout)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    
                    # Parse the source code using BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract the plain text content
                    text = soup.get_text()
                    
                    # Clean up the text - remove extra whitespace and empty lines
                    lines = (line.strip() for line in text.splitlines())
                    text = '\n'.join(line for line in lines if line)
                    
                    # Get page title if available
                    title_tag = soup.find('title')
                    page_title = title_tag.get_text().strip() if title_tag else "Webpage Content"
                    
                    result = SearchResult(
                        title=f"result for {url} is page {page_title}",
                        query=url,
                        summary=text
                    )
                    
                    logger.info(f"Successfully extracted content from: {url}")
                    return result
                    
                except requests.exceptions.Timeout:
                    logger.error(f"Timeout error while reading: {url}")
                    default_result = SearchResult(
                        title="Timeout Error",
                        query=url,
                        summary=f"Request timed out after {self.timeout} seconds"
                    )
                    continue
                    
                except requests.exceptions.ConnectionError:
                    logger.error(f"Connection error while reading: {url}")
                    default_result = SearchResult(
                        title="Connection Error",
                        query=url,
                        summary="Unable to establish connection to the webpage"
                    )
                    continue
                    
                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTP error while reading {url}: {e}")
                    default_result = SearchResult(
                        title=f"HTTP Error {e.response.status_code}",
                        query=url,
                        summary=f"HTTP Error: {e.response.status_code} - {e.response.reason}"
                    )
                    continue
                    
                except Exception as e:
                    logger.exception(f"An error occurred while reading the webpage: {e}")
                    continue
                
        return default_result
    
    def search(self, query: Union[List[str], str]) -> List[SearchResult]:
        # Handle single string input by converting to list
        if isinstance(query, str):
            queries = [query]
        
        results = []
        
        for url in query:
            result = self.get_and_format(url)
            results.append(result)
        
        logger.info(f"Processed {len(query)} URLs, got {len(results)} results")
        return results

if __name__ == '__main__':
    # Create an instance of the ReadWebPage class
    reader = ReadWebPage()
    
    urls = [
        "https://api.slingacademy.com/v1/examples/sample-page.html",
        "https://example.com"
    ]

    for url in urls:
        result = reader.search(url)
        if result and result[0].summary:
            print(f"Content from '{url}':")
            print(f"Title: {result[0].title}")
            print(f"Content preview: {result[0].summary[:200]}...")
            print("-" * 50)
        else:
            print(f"No content found for '{url}'\n")