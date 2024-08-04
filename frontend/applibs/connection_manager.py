
import logging
from typing import Any, Dict, Optional
from httpx import AsyncClient, Response
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

class EntweniSDKClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
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

    async def home_home_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/home'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def signup_register_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/register'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def register_register__post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/register/'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def me_me_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/me'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def sign_in_login_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/login'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def login_login__post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/login/'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def google_login_google_login__get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/google-login/'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def callback_callback_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/callback'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def refresh_refresh__post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/refresh/'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def logout_logout__post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/logout/'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def organisations_organisations_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def create_organisation_organisations_post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def organisation_detail_organisations__organisation_id__get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations/{organisation_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def organisation_update_organisations__organisation_id__put(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations/{organisation_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("PUT", url, json=data)
        return response.json()

    async def organisation_deactivate_organisations__organisation_id__deactivate_post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations/{organisation_id}/deactivate'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def organisation_reactivate_organisations__organisation_id__reactivate_post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations/{organisation_id}/reactivate'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def organisation_delete_organisations__organisation_id__delete_delete(self, data: Optional[BaseModel] = None) -> Any:
        url = '/organisations/{organisation_id}/delete'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("DELETE", url, json=data)
        return response.json()

    async def list_bookings_bookings_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/bookings'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def create_booking_bookings_post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/bookings'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def read_booking_bookings__booking_id__get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/bookings/{booking_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def update_booking_bookings__booking_id__put(self, data: Optional[BaseModel] = None) -> Any:
        url = '/bookings/{booking_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("PUT", url, json=data)
        return response.json()

    async def delete_booking_bookings__booking_id__delete(self, data: Optional[BaseModel] = None) -> Any:
        url = '/bookings/{booking_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("DELETE", url, json=data)
        return response.json()

    async def read_products_products_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/products'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def create_product_products_post(self, data: Optional[BaseModel] = None) -> Any:
        url = '/products'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("POST", url, json=data)
        return response.json()

    async def get_product_products__product_id__get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/products/{product_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()

    async def update_product_products__product_id__put(self, data: Optional[BaseModel] = None) -> Any:
        url = '/products/{product_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("PUT", url, json=data)
        return response.json()

    async def delete_product_products__product_id__delete(self, data: Optional[BaseModel] = None) -> Any:
        url = '/products/{product_id}'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("DELETE", url, json=data)
        return response.json()

    async def healthcheck_healthcheck_get(self, data: Optional[BaseModel] = None) -> Any:
        url = '/healthcheck'
        if data:
            data = data.model_dump() if isinstance(data, BaseModel) else data
        response = await self.request("GET", url, json=data)
        return response.json()
