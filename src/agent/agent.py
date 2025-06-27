from src.config.logging import logger
from src.config.setup import config
from src.llm.model import Model
from src.tools.tool import Tool
from src.types.models import Message, Choice, APIToolSchema, InputSchema, ContentBlock, SearchResult
from src.types.typing import Name, Observation
from typing import Optional, List, Dict, Callable
from src.utils.io import read_file, write_to_file


class Agent:
    def __init__(self) -> None:
        self.model = Model(config.MODEL_NAME)
        self.tools: Dict[Name, Tool] = {}
        self.messages: List[Message] = []
        self.system_prompt = read_file(config.PROMPT_TEMPLATE_PATH)
        self.query = ""
        self.max_iterations = 5
        self.current_iteration = 0
        self.summarize_template = read_file(config.SUMMARIZE_TEMPLATE_PATH)

    def register(self, name: Name, func: Callable[[str], str], description: str = "Argument to search", input_schema: InputSchema = InputSchema()) -> None:
        self.tools[name] = Tool(name, func, description, input_schema)

    def trace(self, role: str, content: str) -> None:
        return
        if role != "system":
            self.messages.append(Message(role=role, content=content))
        write_to_file(path=config.OUTPUT_TRACE_PATH, content=f"{role}: {content}\n")

    def think(self, reason_chain: Optional[Message]) -> Message:
        """Main thinking method that handles iteration logic and coordinates the thinking process."""
        self.current_iteration += 1
        logger.info(f"Starting iteration {self.current_iteration}")
        write_to_file(path=config.OUTPUT_TRACE_PATH, content=f"\n{'='*50}\nIteration {self.current_iteration}\n{'='*50}\n")

        if self.current_iteration > self.max_iterations:
            logger.warning("Reached maximum iterations. Stopping.")
            #self.trace("assistant", "I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations.")
            return self.decide({
                "stop_reason": "error",
                "content": "max_iteraction_reached : I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations."
            })
        
        # Prepare the user query message
        prompt = Message(
            role="user",
            content=self.query
        )
        if reason_chain:
            self.add_message(reason_chain)
        else:
            self.add_message(prompt)
        
        # Query the LLM and get response
        response = self.query_llm()
        
        #("assistant", f"Thought: {response}")
        return self.decide(response)

    
    def _is_valid_response(self, response: Dict) -> bool:
        if not isinstance(response, dict):
            return False
        
        # Check for required fields
        required_fields = ['content', 'stop_reason']
        for field in required_fields:
            if field not in response:
                logger.warning(f"Missing required field: {field}")
                return False
        
        return True
    
    def print_message(self, message: Message) -> None:
        print("======================================")
        if isinstance(message.content, str):
            print(f"{message.role}: {message.content}")
        else:
            print(f"{message.role}: {''.join(block.text for block in message.content)}")

    
    def _normalize_content(self, content) -> List[ContentBlock]:
        if isinstance(content, list):
            return [item if isinstance(item, ContentBlock) else ContentBlock(text=str(item)) for item in content]
        elif isinstance(content, ContentBlock):
            return [content]
        else:
            return [ContentBlock(text=str(content))]

    def add_message(self, new_message: Message):
        if not self.messages:
            self.messages.append(new_message)
            return
        
        last_message = self.messages[-1]
        
        if last_message.role == new_message.role:
            last_content = self._normalize_content(last_message.content)
            new_content = self._normalize_content(new_message.content)
            
            # Merge the content
            last_message.content = last_content + new_content
        else:
            self.messages.append(new_message)

    def _create_and_print_message(self, content: str, add_to_messages: bool = False) -> Message:
        message = Message(role="assistant", content=content)
        self.print_message(message)
        if add_to_messages:
            self.add_message(message)
        return message


    def decide(self, response: Dict) -> Message:
        stop_reason = response.get('stop_reason')
        content_blocks = response.get('content', [])

        if stop_reason is None:
            logger.warning("No stop_reason found in response")
            #self.trace("assistant", "I received an incomplete response. Let me try again.")
            return self._create_and_print_message("Incomplete response received. Retrying.")

        if stop_reason == 'tool_use':
            # Handle tool usage
            tool_use_block = None
            for content_block in content_blocks:
                if content_block.get('type') == 'tool_use':
                    tool_use_block = content_block
                    break
            
            if tool_use_block:
                tool_name = tool_use_block.get('name')
                tool_input = tool_use_block.get('input', {})
                act_result = self.act(tool_name, tool_input)
                formatted_result = [obj.model_dump() for obj in act_result]
                response_msg = self._create_and_print_message(
                    f"Used {tool_name}, results: {formatted_result}. Considering next action."
                )
                return self.think(response_msg)
        elif stop_reason == 'end_turn':
            # Handle direct response
            assistant_answer = Message(
                role="assistant",
                content=[ContentBlock(**content) for content in content_blocks]
            )
            self.add_message(assistant_answer)
            self.print_message(assistant_answer)
            return assistant_answer
        elif stop_reason == 'max_tokens':
            #Summarize the messages
            last_item = self.messages.pop()
            summary_message = self.summarize()
            if summary_message.content.startswith('error_summarizing: '):
                return self._create_and_print_message(summary_message.content)
            return self.think(last_item)
        elif stop_reason == 'error':
            return self._create_and_print_message(f"I received an error {response['content']}.")
        else:
            logger.warning(f"Unknown stop_reason: {stop_reason}")
            response_msg = self._create_and_print_message(
                f"Unexpected response type: {stop_reason}. Response: {str(response)}. Retrying."
            )
            return self.think(response_msg)

        response_msg = self._create_and_print_message(
            f"No action taken... please check again"
        )
        return response_msg

    def act(self, tool_name: Name, tool_input: Dict) -> List[SearchResult]: 
        query_value = ""
        tool_str = tool_name.__str__()
        if 'query' in tool_input:
            query_value = tool_input['query']

        if not tool_str or tool_str not in self.tools:
            return [
                SearchResult(
                    title=f"There is no tool for {tool_str}",
                    query=query_value,
                    summary=""
                )
            ]
        
        return self.tools[tool_str].use(query_value)

    def summarize(self) -> Message:
        content = self.messages
        summarize_prompt = Message(
            role="user",
            content=self.summarize_template
        )
        response = self.query_llm()

        if response['stop_reason'] == 'error':
            return Message(
                role="assistant",
                content=f"error_summarizing: {response['content']}"
            )
        assistant_text = ''.join([item['text'] for item in response['content'] if item['type'] == 'text'])
        summarized_content = Message(
            role="assistant",
            content=assistant_text
        )
        self.messages = [summarized_content]
        return summarized_content

    def execute(self, query: str) -> Message: 
        self.current_iteration = 0
        self.query = query
        return self.think(None)

    def query_llm(self) -> Dict:
        max_retries = 3
        #print([tool.api_object.model_dump for tool in self.tools.values()])

        if len(self.messages) > 0:
            last_message = self.messages[-1]
            if last_message.role == "assistant":
                default_user_message = Message(
                    role="user",
                    content="With all the information gather, based on the query I've given, do you need more information from the tools? if not answer if you already have the information needed"
                )
                self.add_message(default_user_message)

        for attempt in range(max_retries):
            try:
                response = self.model.generate(
                    messages=self.messages,
                    tool_list=[tool.api_object for tool in self.tools.values()],
                    system_prompt=self.system_prompt
                )
                logger.info(f"Thinking => {response}")
                
                # Validate response structure
                if not self._is_valid_response(response):
                    logger.warning(f"Invalid response structure on attempt {attempt + 1}: {response}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise Exception("Max retries reached, check the response again")
                
                return response
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying... ({attempt + 2}/{max_retries})")
                    continue
                else:
                    logger.error("Failed after all retries")
                    #self.trace("assistant", f"I encountered an error: {str(e)}. Please try again.")
                    return {
                        'stop_reason': 'error',
                        'content': f"I encountered an error: {str(e)}. Please try again."
                    }