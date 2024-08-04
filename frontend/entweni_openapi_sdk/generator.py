import asyncio

from main import generate_and_save_client

schema_url = "http://localhost:8000/api/v1/docs/openapi.json"  # Replace with your actual schema URL
base_url = "http://localhost:8000/api/v1"  # Replace with your actual API base URL
output_file = "applibs/connection_manager.py"  # Path to save the generated client

asyncio.run(generate_and_save_client(schema_url, base_url, output_file))
