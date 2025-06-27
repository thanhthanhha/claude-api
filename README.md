# AI Agent - Web Search & Research Tool

An intelligent AI agent system that combines large language models with web search capabilities to perform autonomous research and information gathering tasks.

## Overview

This project implements an AI agent that can think, act, and decide using various tools to answer complex queries. The agent uses a reasoning loop to iteratively gather information, make decisions, and provide comprehensive answers.

## Key Features

- **Autonomous Reasoning**: Multi-iteration thinking process with configurable limits
- **Tool Integration**: Seamless integration with web search, Wikipedia, and webpage reading tools
- **LLM Integration**: Uses AWS Bedrock models for natural language processing
- **Message Management**: Intelligent conversation history management with summarization
- **Error Handling**: Robust retry mechanisms and error recovery
- **Configurable**: YAML-based configuration system

## Architecture

### Core Components

#### Agent (`src/agent/agent.py`)
The main orchestrator that implements the think-act-decide loop:
- **Think**: Processes queries and coordinates the reasoning process
- **Act**: Executes tools based on decisions made during thinking
- **Decide**: Determines next actions based on LLM responses and tool results

#### Configuration (`src/config/setup.py`)
Manages application settings loaded from `/config/config.yaml`:
- Model selection and parameters
- File paths and templates
- System behavior configuration

#### LLM Integration (`src/llm/model.py`)
Handles communication with AWS Bedrock models:
- Message formatting and processing
- Tool schema integration
- Response parsing and validation

#### Tools (`src/tools/`)
Extensible tool system including:
- **Wikipedia Search**: Access to Wikipedia articles
- **Google Search**: Web search capabilities
- **Web Page Reader**: Extract content from web pages

#### Data Types (`src/types/models.py`)
Comprehensive data structures for:
- Messages and conversation history
- Tool schemas and responses
- Search results and content blocks
- API responses and choices

#### Utilities (`src/utils/data.py`)
Data preprocessing and utility functions for:
- File I/O operations
- Data transformation
- Content processing

## How It Works

1. **Query Processing**: User provides a query to the agent
2. **Iterative Reasoning**: Agent enters a think-act-decide loop:
   - **Think**: Analyzes the query and current context
   - **Act**: Uses appropriate tools to gather information
   - **Decide**: Determines if more information is needed or if ready to respond
3. **Tool Execution**: Agent dynamically selects and executes relevant tools
4. **Response Generation**: Synthesizes gathered information into a comprehensive answer
5. **Memory Management**: Automatically summarizes conversation history when limits are reached

## Usage Example

```python
from src.agent.agent import Agent

# Initialize agent
agent = Agent()

# Register tools (automatically configured)
# Tools include: wiki_search, google_search, read_webpage

# Execute query
result = agent.execute("What are the latest developments in renewable energy?")
print(result.content)
```

## Configuration

The system uses YAML configuration files to manage:
- Model parameters and selection
- Maximum iteration limits
- File paths for templates and outputs
- Tool-specific settings

## Key Benefits

- **Autonomous Operation**: Minimal human intervention required
- **Comprehensive Research**: Combines multiple information sources
- **Scalable Architecture**: Easy to add new tools and capabilities
- **Robust Error Handling**: Graceful failure recovery and retry mechanisms
- **Flexible Configuration**: Easily adaptable to different use cases

## Technical Highlights

- **Message Merging**: Intelligent conversation history management
- **Tool Schema Validation**: Type-safe tool integration
- **Iterative Refinement**: Multi-step reasoning for complex queries
- **Content Summarization**: Automatic context compression for long conversations
- **Extensible Design**: Plugin-style architecture for adding new capabilities

This AI agent system provides a powerful foundation for building intelligent research assistants that can autonomously gather, process, and synthesize information from multiple web sources.