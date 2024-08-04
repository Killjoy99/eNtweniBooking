from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.decorators import check_accept_header, render_template
from src.database.core import get_async_db

from .models import Product

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("", name="read_products")
@render_template(template_name="product/list.html")
async def get_products(
    request: Request,
    is_template: Optional[bool] = Depends(check_accept_header),
    db: AsyncSession = Depends(get_async_db),
):
    """Get all products."""
    statement = await db.execute(select(Product))
    products = statement.scalars().all()

    if is_template:
        return {"data": products, "error_message": None}
    else:
        return products


@product_router.post("", name="create_product")
async def create_product():
    return {"detail": "Create Product success"}


@product_router.get("/{product_id}")
async def get_product(product_id: int):
    return {"detail": f"Product {product_id} details"}


@product_router.put("/{product_id}", name="update_product")
async def update_product(product_id: int):
    return {"detail": f"Updated product {product_id}"}


@product_router.delete("/{product_id}", name="delete_product")
async def delete_product(product_id: int):
    return {"detail": f"Deleted product {product_id}"}
