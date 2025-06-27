from src.config.logging import logger
from src.config.setup import config
from src.types.models import SearchResult
from typing import List
import requests
import os


class GoogleSearcher:
    """Google Custom Search API wrapper class"""
    
    def __init__(self, num_results=10):
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.api_key = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
        self.cx = config.CUSTOMSEARCH_ID
        self.num_results = num_results
        
        if not self.api_key:
            raise ValueError("GOOGLE_CUSTOM_SEARCH_API_KEY environment variable not set")
        
        if not self.cx:
            raise ValueError("CUSTOMSEARCH_ID not found in config")
    
    def search(self, query, num_results=None) -> List[SearchResult]:
        default_result = [SearchResult(
            title=f"No information found for {query}",
            query=query,
            summary=""
        )]
        if not query or not query.strip():
            logger.warning("Empty query provided to search method")
            return default_result
        
        # Use provided num_results or fall back to instance default
        results_count = num_results if num_results is not None else self.num_results
        
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query.strip(),
            'num': results_count
        }
        
        logger.info(f"Searching for query: '{query}' with params: {params}")
        
        try:
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = []

                #print(data)
                
                for item in data.get('items', []):
                    try:
                        result = SearchResult(
                            title=f"title: {item.get('title', 'No title')} - url: {item.get('link', 'No url found')}",
                            query=query,
                            summary=item.get('snippet', '')
                        )
                        results.append(result)
                    except Exception as e:
                        logger.warning(f"Failed to create SearchResult for item: {e}")
                        continue
                
                logger.info(f"Successfully retrieved {len(results)} results for query: '{query}'")
                if results == []:
                    return default_result
                return results
            else:
                logger.error(f"Search failed with status {response.status_code}")
                try:
                    error_data = response.json()
                    logger.error(f"Error response: {error_data}")
                except:
                    logger.error(f"Error response text: {response.text}")
                return default_result
                
        except requests.RequestException as e:
            logger.error(f"Request failed for query '{query}': {str(e)}")
            return default_result
        except Exception as e:
            logger.error(f"Unexpected error during search for query '{query}': {str(e)}")
            return default_result


if __name__ == '__main__':
    # Usage example
    try:
        searcher = GoogleSearcher(num_results=10)
        queries = ["Geoffrey Hinton", "Demis Hassabis"]

        for query in queries:
            result = searcher.search(query)
            if result:
                print(f"JSON result for '{query}':\n{result}\n")
            else:
                print(f"No result found for '{query}'\n")
                
    except Exception as e:
        print(f"Failed to initialize GoogleSearcher: {e}")