import logging
import os

from openapi_schema_pydantic import OpenAPI, Operation

logging.basicConfig(level=logging.INFO)


def generate_models(schema: OpenAPI) -> str:
    """Generate Pydantic model classes based on the OpenAPI schema definitions."""
    model_code = """
from typing import Any, Dict, Optional
from pydantic import BaseModel

    
    """

    for model_name, model_schema in schema.components.schemas.items():
        fields = []
        for prop_name, prop_schema in model_schema.properties.items():
            pydantic_type = "Any"  # Default type
            if "type" in prop_schema:
                if prop_schema["type"] == "string":
                    pydantic_type = "str"
                elif prop_schema["type"] == "integer":
                    pydantic_type = "int"
                elif prop_schema["type"] == "number":
                    pydantic_type = "float"
                elif prop_schema["type"] == "boolean":
                    pydantic_type = "bool"
                elif prop_schema["type"] == "array":
                    item_type = prop_schema["items"].get("type", "Any")
                    pydantic_type = f"List[{item_type}]"
                elif prop_schema["type"] == "object":
                    pydantic_type = "Dict[str, Any]"
            fields.append(f"{prop_name}: {pydantic_type}")

        model_code += f"""
class {model_name}(BaseModel):
    {'\n    '.join(fields)}
"""

    return model_code


def generate_client_code(
    schema: OpenAPI, base_url: str = "http://localhost:8000"
) -> str:
    """Generate Python code for a client based on the OpenAPI schema."""

    def create_method_code(method: str, path: str, operation: Operation) -> str:
        func_name = (
            operation.operationId or f"{method}_{path.replace('/', '_')}".lower()
        )
        func_name = func_name.replace("{", "").replace(
            "}", ""
        )  # Simplify function name
        func_code = f"""
    async def {func_name}(self, data: Optional[BaseModel] = None) -> Any:
        url = '{path}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("{method.upper()}", url, json=data)
        return response.json()
"""
        return func_code

    class_code = (
        """
import logging
from typing import Any, Dict, Optional
from httpx import AsyncClient, Response
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

class EntweniSDKClient:
    def __init__(self, base_url: str = "%s"):
        self.base_url = base_url
        self.client = AsyncClient(base_url=base_url)

    async def request(self, method: str, url: str, json: Optional[Dict[str, Any]] = None) -> Response:
        try:
            response: Response = await self.client.request(
                method=method, url=url, json=json
            )
            response.raise_for_status()
            return response
        except Exception as e:
            logging.error(f"Request failed: {e}")
            raise

    async def close(self):
        await self.client.aclose()
"""
        % base_url
    )

    # Generate methods for each path and operation
    for path, path_item in schema.paths.items():
        for method in path_item.__fields_set__:
            operation: Operation = getattr(path_item, method)
            class_code += create_method_code(method, path, operation)

    return class_code


def write_client_and_models(code: str, models_code: str, folder_path: str):
    """Write the generated code to Python files in the specified folder."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    main_file = os.path.join(folder_path, "main.py")
    models_file = os.path.join(folder_path, "models.py")
    init_file = os.path.join(folder_path, "__init__.py")

    # Write the client code to main.py
    with open(main_file, "w") as file:
        file.write(code)

    # Write the models code to models.py
    with open(models_file, "w") as file:
        file.write(models_code)

    # Create an empty __init__.py
    # import the sdk in the init file
    with open(init_file, "w") as file:
        file.write("from .main import EntweniSDKClient")


async def generate_and_save_client(schema_url: str, base_url: str, output_folder: str):
    from httpx import AsyncClient

    async with AsyncClient() as client:
        response = await client.get(schema_url)
        response.raise_for_status()
        schema_data = response.json()

    schema = OpenAPI.model_validate(schema_data)
    client_code = generate_client_code(schema, base_url)
    models_code = generate_models(schema)
    write_client_and_models(client_code, models_code, output_folder)
