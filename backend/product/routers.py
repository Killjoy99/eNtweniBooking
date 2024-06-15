from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, AsyncSession
from database.core import get_db


product_router = APIRouter()


@product_router.get("", name="read_products")
async def get_products():
    return {"detail": "List of Products"}


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
