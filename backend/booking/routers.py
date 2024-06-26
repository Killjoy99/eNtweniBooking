from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from database.core import get_db
from core.decorators import check_accept_header, render_template, return_json

from .models import Booking
from .schemas import BookingCreate, BookingRead


booking_router = APIRouter()


@booking_router.get("")
async def list_bookings(request: Request, is_template: Optional[bool]=Depends(check_accept_header), db: async_sessionmaker[AsyncSession] = Depends(get_db)):
    """Get all bookings."""
    statement = await db.execute(select(Booking))
    bookings = statement.scalars().all()
    data = {"bookings": bookings}
    # data = {}
    
    if is_template:
        return render_template(request=request, template_name="product/list.html", context=data)
    else:
        return bookings


@booking_router.post("", name="create_booking")
async def create_booking():
    return {"detail": "Created a booking with ID [_id]"}


@booking_router.get("/{booking_id}", name="read_booking")
async def get_booking_details(id: int):
    return {"detail": f"Booking Details for a booking with ID:{id}"}

@booking_router.put("/{booking_id}", name="update_booking")
async def update_booking(id: int):
    return {"detail": f"Updated Booking with ID: {id}"}

@booking_router.delete("/{booking_id}", name="delete_booking")
async def delete_booking(id:int):
    # Adjust all deletes to be soft deletes
    return {"detail": f"Deleted organisation with ID:{id}"}