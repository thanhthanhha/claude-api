from src.types.typing import Name, Observation 
from src.types.models import APIToolSchema, InputSchema
from typing import Callable

class Tool:
    def __init__(self, name: Name, func: Callable[[str], str], description: str = "Argument to search", input_schema: InputSchema = InputSchema()):
            self.name = name
            self.func = func
            self.api_object = APIToolSchema(
                name=self.name.__str__(),
                description=description,
                input_schema=input_schema
            )

    def use(self, query: str) -> Observation:
        try:
            return self.func(query)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return str(e)