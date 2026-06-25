from fastapi import APIRouter, Request, Form, Depends, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.database import models
from app.core.security import create_token, verify_token
from app.core.config import ADMIN_USERNAME, ADMIN_PASSWORD
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "admin_login.html",
        {
            "request": request
        }
    )


@router.post("/admin/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        token = create_token({"sub": username})

        response = RedirectResponse(
            url="/admin/dashboard",
            status_code=302
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True
        )

        return response

    # Wrong credentials
    return templates.TemplateResponse(
        "admin_login.html",
        {
            "request": request,
            "error": "Invalid Username or Password"
        }
    )


"""
@router.get("/admin/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/admin/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = create_token({"sub": username})
        response = RedirectResponse("/admin/dashboard", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response

    return {"error": "Invalid credentials"} """

@router.get("/admin/dashboard")
def dashboard(request: Request, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token or not verify_token(access_token):
        return RedirectResponse("/admin/login")

    bookings = db.query(models.Booking).all()

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "bookings": bookings
    })

def _get_booking_or_none(db: Session, booking_id: int):
    return db.query(models.Booking).get(booking_id)


@router.get("/admin/edit/{id}")
def edit_booking_page(id: int, request: Request, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token or not verify_token(access_token):
        return RedirectResponse("/admin/login")

    booking = _get_booking_or_none(db, id)
    if not booking:
        return RedirectResponse("/admin/dashboard", status_code=302)

    # booking.date is stored as DD/MM/YYYY; convert for HTML date input (YYYY-MM-DD)
    try:
        from datetime import datetime

        date_for_input = datetime.strptime(booking.date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except Exception:
        date_for_input = ""

    return templates.TemplateResponse(
        "admin_edit_booking.html",
        {
            "request": request,
            "booking": booking,
            "date_for_input": date_for_input,
        },
    )


@router.post("/admin/edit/{id}")
def update_booking(
    id: int,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    event_type: str = Form(...),
    guests: int = Form(...),
    date: str = Form(...),
    time_slot: str = Form(...),
    message: str = Form(""),
    access_token: str = Cookie(None),
    db: Session = Depends(get_db),
):
    if not access_token or not verify_token(access_token):
        return RedirectResponse("/admin/login")

    booking = _get_booking_or_none(db, id)
    if not booking:
        return RedirectResponse("/admin/dashboard", status_code=302)

    error = None

    allowed_events = ["Wedding", "Corporate", "Birthday"]
    if event_type not in allowed_events:
        error = "Invalid event type selected."

    allowed_slots = ["Morning", "Afternoon", "Night"]
    if time_slot not in allowed_slots:
        error = "Invalid time slot selected."

    try:
        from datetime import datetime

        event_date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        if event_date_obj < datetime.today().date():
            error = "Date cannot be in the past."
        indian_date = event_date_obj.strftime("%d/%m/%Y")
    except ValueError:
        error = "Invalid date format."

    if error:
        # re-render with same booking object, but keep date input populated from user input
        return templates.TemplateResponse(
            "admin_edit_booking.html",
            {
                "request": request,
                "booking": booking,
                "date_for_input": date,
                "error": error,
            },
        )

    booking.name = name
    booking.email = email
    booking.phone = phone
    booking.event_type = event_type
    booking.guests = guests
    booking.date = indian_date
    booking.time_slot = time_slot
    booking.message = message

    db.commit()

    # show success on edit page
    return templates.TemplateResponse(
        "admin_edit_booking.html",
        {
            "request": request,
            "booking": booking,
            "date_for_input": date,
            "success": "Booking updated successfully.",
        },
    )


@router.post("/admin/delete/{id}")
def delete_booking(id: int, db: Session = Depends(get_db), access_token: str = Cookie(None)):
    if not access_token or not verify_token(access_token):
        return RedirectResponse("/admin/login")

    booking = _get_booking_or_none(db, id)
    if booking:
        db.delete(booking)
        db.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)


@router.get("/admin/logout")
def logout():
    response = RedirectResponse("/admin/login")
    response.delete_cookie("access_token")
    return response