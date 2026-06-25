from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/services")
def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@router.get("/menu")
def menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/gallery")
def gallery(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})

@router.get("/alumni")
def alumni(request: Request):
    return templates.TemplateResponse("alumni.html", {"request": request})

@router.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )