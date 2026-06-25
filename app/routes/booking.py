from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database import models
from app.services.email_service import send_email

from datetime import datetime, timedelta
import re

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -----------------------
# DB Dependency
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# GET BOOKING PAGE
# -----------------------
@router.get("/booking")
def booking_page(request: Request):
    return templates.TemplateResponse(
        "booking.html",
        {"request": request}
    )


# -----------------------
# POST BOOKING
# -----------------------
@router.post("/booking")
async def create_booking(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    event_type: str = Form(...),
    guests: int = Form(...),
    date: str = Form(...),
    time_slot: str = Form(...),
    message: str = Form(""),
    db: Session = Depends(get_db)
):

    error = None

    # -----------------------
    # Name Validation
    # -----------------------
    if len(name.strip()) < 2:
        error = "Name must contain at least 2 characters."

    # -----------------------
    # Email Validation
    # -----------------------
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(email_pattern, email):
        error = "Please enter a valid email address."

    # -----------------------
    # Phone Validation
    # -----------------------
    if not phone.isdigit():
        error = "Phone number must contain digits only."

    elif len(phone) != 10:
        error = "Phone number must contain exactly 10 digits."

    # -----------------------
    # Event Type Validation
    # -----------------------
    allowed_events = [
        "Wedding",
        "Corporate",
        "Birthday"
    ]

    if event_type not in allowed_events:
        error = "Invalid event type selected."

    # -----------------------
    # Time Slot Validation
    # -----------------------
    allowed_slots = [
        "Morning",
        "Afternoon",
        "Night"
    ]

    if time_slot not in allowed_slots:
        error = "Invalid time slot selected."

    # -----------------------
    # Guests Validation
    # -----------------------
    if guests < 1:
        error = "Guest count must be greater than zero."

    # -----------------------
    # Date Validation
    # -----------------------
    try:

        event_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()

        minimum_date = (
            datetime.today().date()
            + timedelta(days=3)
        )

        if event_date < minimum_date:
            error = (
                "Event date must be at least "
                "3 days after today."
            )

        indian_date = event_date.strftime(
            "%d/%m/%Y"
        )

    except ValueError:
        error = "Invalid date format."

    # -----------------------
    # Return Error Popup
    # -----------------------
    if error:
        return templates.TemplateResponse(
            "booking.html",
            {
                "request": request,
                "error": error
            }
        )

    # -----------------------
    # Save Booking
    # -----------------------
    booking = models.Booking(
        name=name,
        email=email,
        phone=phone,
        event_type=event_type,
        guests=guests,
        date=indian_date,
        time_slot=time_slot,
        message=message
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    # -----------------------
    # Email
    # -----------------------
    await send_email(
        email,
        "Booking Confirmed 🎉",
        f"""
        <h2>Booking Confirmed</h2>

        <p>Hello {name},</p>

        <ul>
            <li>Event : {event_type}</li>
            <li>Date : {indian_date}</li>
            <li>Time : {time_slot}</li>
            <li>Guests : {guests}</li>
        </ul>

        <p>Thank you for booking with us.</p>
        """
    )

    return templates.TemplateResponse(
        "booking.html",
        {
            "request": request,
            "success":
            f"Booking successful for {indian_date} ({time_slot})"
        }
    )