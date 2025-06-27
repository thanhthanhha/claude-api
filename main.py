from src.agent.agent import Agent
from src.tools.google import GoogleSearcher
from src.tools.wiki import WikipediaSearcher
from src.tools.readwebpage import ReadWebPage
from src.config.static import google_search_properties, wiki_search_properties, webpage_search_properties
from src.types.models import InputSchema

def main():
    # Initialize the agent and tools
    agent = Agent()
    google_searcher = GoogleSearcher()
    wiki_searcher = WikipediaSearcher()
    read_web_page = ReadWebPage()

    # Create input schemas
    google_input_schema = InputSchema(properties=google_search_properties, required=["query"])
    wiki_input_schema = InputSchema(properties=wiki_search_properties, required=["query"])
    webpage_input_schema = InputSchema(properties=webpage_search_properties, required=["query"])

    # Register tools with the agent
    agent.register("google_search", google_searcher.search, "Search Google for up-to-date information", google_input_schema)
    agent.register("wikipedia_search", wiki_searcher.search, "Search Wikipedia for people, places, phenomenon. Note that we should only search the full name of people or places like \"Harry Style\" \"Paris\" multiple name in one search is not supported", wiki_input_schema)
    agent.register("read_web_page", read_web_page.search, "Read the text content of a web page when an url is provided. Note that if a page is unaccessible retry until it work", webpage_input_schema)

    print("Chat Console Started. Type '/quit' to exit.")
    print("=" * 40)
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if query.lower() == '/quit':
                print("Goodbye!")
                break
            
            if not query:
                continue
                
            print("Agent:", end=" ")
            agent.execute(query)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()