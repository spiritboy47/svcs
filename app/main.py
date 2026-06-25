from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.database.connection import engine, Base
from app.routes import admin, booking, pages

# -----------------------------
# Create DB Tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# App Init with API Docs
# -----------------------------
app = FastAPI(
    title="SVCS Catering API 🍽",
    description="API for Siddi Vinayaka Catering Service (Bookings, Admin, Contact)",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
    openapi_url="/openapi.json"
)

# -----------------------------
# Base Directory (IMPORTANT)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Static Files (FIXED)
# -----------------------------
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(pages.router, tags=["Pages"])
app.include_router(booking.router, tags=["Booking"])
app.include_router(admin.router, tags=["Admin"])