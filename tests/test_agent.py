from src.agent.agent import Agent
from src.tools.google import GoogleSearcher
from src.tools.wiki import WikipediaSearcher

def main():
    # Initialize the agent
    agent = Agent()

    # Initialize the search tools
    google_searcher = GoogleSearcher()
    wiki_searcher = WikipediaSearcher()

    # Register the search tools with the agent
    agent.register("google_search", google_searcher.search, "Search Google for up-to-date information")
    agent.register("wikipedia_search", wiki_searcher.search, "Search Wikipedia for people, places, phenomena")

    # Define the query
    query = "Who is Neil Perry from Dead Poets Society? And where is the actor now? Is he dead or alive?"

    print(f"Question: {query}")
    print("=" * 50)

    # Execute the query
    agent.execute(query)

    # Print the answer
    # print("Answer:")
    # print(response.content if hasattr(response, 'content') else str(response))

if __name__ == "__main__":
    main()
