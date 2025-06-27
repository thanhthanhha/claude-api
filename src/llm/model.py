import boto3
import json
from botocore.exceptions import ClientError
from src.config.logging import logger
from src.config.setup import config
from src.types.models import Message, AnthropicAPIBody
from src.types.models import APIToolSchema, InputSchema
from typing import List


class Model:
    def __init__(self, model_id="amazon.titan-text-express-v1"):
        self.model_id = model_id
        self.region_name = config.REGION
        self.client = self._init_client()
        print(config.REGION)
        try:
            print(config.MODEL_CONFIG)
            self.validate_config(config.MODEL_CONFIG)
            self.__dict__.update(config.MODEL_CONFIG)
        except (ClientError, Exception) as e:
            logger.exception(e)
            raise
        self.config = config.MODEL_CONFIG

    def _init_client(self):
        try:
            return boto3.client("bedrock-runtime", region_name=self.region_name)
        except Exception as e:
            logger.error(f"Can't initialize Bedrock client. Reason: {e}")
            raise
    
    def validate_config(self, config):
        allowed_params = {"max_tokens", "temperature", "top_p", "top_k"}
        
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        
        invalid_params = set(config.keys()) - allowed_params
        
        if invalid_params:
            logger.error(f"Invalid configuration parameters found: {invalid_params}")
            raise ValueError(f"Invalid configuration parameters: {list(invalid_params)}. "
                           f"Allowed parameters are: {list(allowed_params)}")
        
        logger.info("Configuration validation passed")
        return True

    def generate(self, messages: List[Message], tool_list: List[APIToolSchema], system_prompt: str = "Proceed to answer as usual"):
        
        # Format the request payload using the model's native structure

        api_request = AnthropicAPIBody(
            anthropic_version="bedrock-2023-05-31",
            max_tokens=self.config['max_tokens'],
            top_k=self.config['top_k'],
            top_p=self.config['top_p'],
            messages=messages,
            tools=tool_list,
            tool_choice={"type": "auto"},
            system=system_prompt
        )
        
        
        # Convert the native request to JSON
        request = api_request.model_dump_json(exclude_none=True)
        
        try:
            # Invoke the model with the request
            response = self.client.invoke_model(modelId=self.model_id, body=request)
            
            # Decode the response body
            model_response = json.loads(response["body"].read())
            
            # Extract and return the response text
            response_content = model_response["content"]
            logger.info(f"Successfully generated response for messages printing response text:\n {model_response}")
            return model_response
            
        except (ClientError, Exception) as e:
            logger.exception(f"Can't invoke '{self.model_id}'. Reason: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    # Initialize the model
    model = Model()
    
    
    # Generate text
    prompt = "Describe the purpose of a 'hello world' program in one line."
    
    try:
        response = model.generate(prompt)
        logger.info(f"Generated response: {response}")
    except Exception as e:
        logger.error(f"Generation failed: {e}")