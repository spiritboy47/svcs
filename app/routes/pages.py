from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )


@router.get("/services")
def services(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="services.html",
        context={}
    )


@router.get("/menu")
def menu(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={}
    )


@router.get("/gallery")
def gallery(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={}
    )


@router.get("/alumni")
def alumni(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="alumni.html",
        context={}
    )


@router.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={}
    )
