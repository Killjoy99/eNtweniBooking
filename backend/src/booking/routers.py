from typing import Optional

from core.utils import check_accept_header
from database.core import get_async_db
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Booking
from .schemas import BookingCreate

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.get("")
async def list_bookings(
    request: Request,
    is_template: Optional[bool] = Depends(check_accept_header),
    db: AsyncSession = Depends(get_async_db),
):
    """Get all bookings."""
    statement = await db.execute(select(Booking))
    bookings = statement.scalars().all()
    data = {"bookings": bookings}
    # data = {}

    if is_template:
        return {"data": data, "error_message": None}
    return bookings


@booking_router.post("", name="create_booking")
async def create_booking(
    request: Request,
    booking: BookingCreate,
    is_template: Optional[bool] = Depends(check_accept_header),
    db: AsyncSession = Depends(get_async_db),
):
    return {"detail": "Created a booking with ID [_id]"}


@booking_router.get("/{booking_id}", name="read_booking")
async def get_booking_details(id: int):
    return {"detail": f"Booking Details for a booking with ID:{id}"}


@booking_router.put("/{booking_id}", name="update_booking")
async def update_booking(id: int):
    return {"detail": f"Updated Booking with ID: {id}"}


@booking_router.delete("/{booking_id}", name="delete_booking")
async def delete_booking(id: int):
    # Adjust all deletes to be soft deletes
    return {"detail": f"Deleted organisation with ID:{id}"}
