from src.config.logging import logger
from typing import Dict
from typing import Any
import yaml
import os


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            # The following line ensures that the __init__ method is only called once.
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = "./config/config.yml"):
        if self.__initialized:
            return
        self.__initialized = True
        
        self.__config = self._load_config(config_path)
        self.PROJECT_ID = self.__config['project_id']
        self.REGION = self.__config['region']
        self.CREDENTIALS_PATH = self.__config['credentials_json']
        self.CUSTOMSEARCH_ID = self.__config['customsearch_id']
        #self._set_google_credentials(self.CREDENTIALS_PATH)
        self.MODEL_NAME = self.__config['model_name']
        self.MODEL_CONFIG = self.__config['model_config']
        self.PROMPT_TEMPLATE_PATH = self.__config['prompt_template_path']
        self.OUTPUT_TRACE_PATH  = self.__config['output_trace_path']
        self.SUMMARIZE_TEMPLATE_PATH = self.__config['summarize_template_path']

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load the configuration file. Error: {e}")

    @staticmethod
    def _set_google_credentials(credentials_path: str) -> None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


config = Config()