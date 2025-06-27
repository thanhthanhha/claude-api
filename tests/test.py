from src.llm.model import Model
from src.tools.wiki import WikipediaSearcher
from src.types.models import Message, ContentBlock, APIToolSchema, InputSchema
from src.types.typing import Name
from src.tools.tool import Tool
from src.config.setup import config


model = Model(config.MODEL_NAME)

# Alternative: specify a different model
# model = Model(model_id="anthropic.claude-3-sonnet-20240229-v1:0")

# Create InputSchema for Wikipedia tool
wiki_input_schema = InputSchema(
    type="object",
    properties={
        "query": {
            "type": "string",
            "description": "Query from Wiki database. For example query about people, places, phenomanon of science,..."
        }
    },
    required=["query"]
)

# Initialize WikipediaSearcher
wiki_searcher = WikipediaSearcher()

# Create Tool object
wiki_tool = Tool(
    name=Name(1),
    func=wiki_searcher.search,
    description="Search Wikipedia for information about people, places, scientific phenomena, and other topics",
    input_schema=wiki_input_schema
)

# The tool's API object is now available as wiki_tool.api_object
print(wiki_tool.api_object.model_dump_json(indent=2))


# Create a message with simple string content
simple_message = Message(
    role="user",
    content="Answer the query and decide if this information require tools or not if not answer the question directly: Whats the up to date information about the movie '28 years later'. Note that when the answer do not need tool, do not mention your reasoning process and provide answer directly"
)

# Create a message with structured content blocks
content_blocks = [
    ContentBlock(type="text", text="Hello! Can you help me with a question?"),
    ContentBlock(type="text", text="What are the benefits of using Python?")
]

structured_message = Message(
    role="user",
    content=content_blocks
)

# Create a simple tool schema (optional)
example_tool = APIToolSchema(
    name="get_weather",
    description="Get current weather information for a location",
    input_schema=InputSchema(
        type="object",
        properties={
            "location": {
                "type": "string",
                "description": "The city and state/country"
            }
        },
        required=["location"]
    )
)

    "query": {
        "type": "string",
        "description": "Query from Wiki database, query about people, places, phenomanon of science,... For example query need to be a specific name like \"france\" \"Butterfly Effect\""
}

    "query": {
        "type": "string",
        "description": "String to query from google"
}
response1 = model.generate(messages=[simple_message],tool_list=[wiki_tool.api_object])
try:
    print("Sending simple message...")
    # Generate response with simple message
    response1 = model.generate(
        messages=[simple_message],
        tool_list=[wiki_tool.api_object]  # No tools
    )
    print(f"Response 1: {response1}")
    print("-" * 50)

    print("Sending structured message...")
    # Generate response with structured message and tools
    response2 = model.generate(
        messages=[structured_message],
        tool_list=[example_tool]
    )
    print(f"Response 2: {response2}")

except Exception as e:
    print(f"Error generating response: {e}")