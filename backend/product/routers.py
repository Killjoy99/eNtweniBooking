from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, AsyncSession
from database.core import get_db

from .models import Product
from .schemas import ProductCreate, ProductRead

from core.decorators import check_accept_header, render_template, return_json


product_router = APIRouter()


@product_router.get("", name="read_products")
async def get_products(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession] = Depends(get_db)):
    """Get all products."""
    statement = await db.execute(select(Product))
    products = statement.scalars().all()
    data = {"products": products}
    # data = {}
    
    if is_template:
        return render_template(request=request, template_name="product/list.html", context=data)
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
