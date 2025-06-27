from src.config.logging import logger
from typing import Optional
import wikipediaapi
from src.types.models import SearchResult
from typing import List
import json


class WikipediaSearcher:
    
    def __init__(self, user_agent: str = 'ReAct Agents (shankar.arunp@gmail.com)', language: str = 'en'):

        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language)
        self.user_agent = user_agent
        self.language = language
    
    def search(self, query: str) -> List[SearchResult]:
        default_result = [SearchResult(
            title=f"No information found for {query}",
            query=query,
            summary=""
        )]
        try:
            logger.info(f"Searching Wikipedia for: {query}")
            page = self.wiki.page(query)

            if page.exists():
                # Create a dictionary with query, title, and summary
                page_content = page.summary
                if 'may refer to:' in page.summary or 'disambiguation' in page.title.lower():
                    page_content = page.text
                result = [
                    SearchResult(
                        title=page.title,
                        query=query,
                        summary=page_content
                    )
                ]
                logger.info(f"Successfully retrieved summary for: {query}")
                return result
            else:
                logger.info(f"No results found for query: {query}")
                return default_result

        except Exception as e:
            logger.exception(f"An error occurred while processing the Wikipedia query: {e}")
            return default_result


if __name__ == '__main__':
    # Create an instance of the WikipediaSearcher
    searcher = WikipediaSearcher()
    
    queries = ["Geoffrey Hinton", "Demis Hassabis"]

    for query in queries:
        result = searcher.search(query)
        if result:
            print(f"JSON result for '{query}':\n{result}\n")
        else:
            print(f"No result found for '{query}'\n")