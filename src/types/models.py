from pydantic import BaseModel, Field
import json
from typing import List, Dict, Any, Optional, Union
from src.types.typing import Name

class ContentBlock(BaseModel):
    type: str = Field(default="text", description="The type of content block.")
    text: str = Field(..., description="The text content of the block.")

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender.")
    content: Union[str, List[ContentBlock]] = Field(..., description="The content of the message.")

class Choice(BaseModel):
    name: Name = Field(..., description="The name of the tool chosen.")
    reason: str = Field(..., description="The reason for choosing this tool.")

class InputSchema(BaseModel):
    type: str = "object"
    properties: Dict[str, Any] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)

class APIToolSchema(BaseModel):
    type: Optional[str] = None
    name: str
    description: str
    input_schema: InputSchema = Field(default_factory=InputSchema)

class AnthropicAPIBody(BaseModel):
    anthropic_version: str = Field(..., description="The version of the Anthropic API.")
    max_tokens: int = Field(..., description="Maximum number of tokens to generate.")
    messages: List[Message] = Field(..., description="List of messages in the conversation.")
    system: Optional[str] = Field(None, description="System prompt to set assistant behavior.")
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nucleus sampling: only consider tokens with cumulative probability up to top_p (0.0-1.0).")
    top_k: Optional[int] = Field(None, ge=1, description="Only consider the top_k most likely tokens at each step.")
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0, description="Controls randomness in responses (0.0-1.0).")
    tools: Optional[List[APIToolSchema]] = Field(None, description="List of available tools for the assistant.")
    tool_choice: Optional[Dict[str, str]] = Field(None, description="Strategy for tool selection.")
    
#Search Models

class SearchResult(BaseModel):
    title: str = Field(..., description="Title of the search result")
    query: str = Field(..., description="Original search query")
    summary: str = Field(default="", description="Snippet/summary of the search result")
    