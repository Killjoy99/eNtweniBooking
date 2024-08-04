import logging

from openapi_schema_pydantic import OpenAPI, Operation

logging.basicConfig(level=logging.INFO)


def generate_client_code(
    schema: OpenAPI, base_url: str = "http://localhost:8000"
) -> str:
    """Generate Python code for a client based on the OpenAPI schema."""

    def create_method_code(method: str, path: str, operation: Operation) -> str:
        func_name = (
            # operation.operationId
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
        for method in path_item.model_fields_set:
            operation: Operation = getattr(path_item, method)
            class_code += create_method_code(method, path, operation)

    return class_code


def write_client_module(code: str, file_path: str):
    """Write the generated code to a Python file."""
    with open(file_path, "w") as file:
        file.write(code)


# Example usage
async def generate_and_save_client(schema_url: str, base_url: str, output_file: str):
    from httpx import AsyncClient

    async with AsyncClient() as client:
        response = await client.get(schema_url)
        response.raise_for_status()
        schema_data = response.json()

    schema = OpenAPI.model_validate(schema_data)
    client_code = generate_client_code(schema, base_url)
    write_client_module(client_code, output_file)
