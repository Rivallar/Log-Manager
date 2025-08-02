"""
Web routes for serving HTML pages using Jinja2 templates
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard homepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/agentlogs", response_class=HTMLResponse)
async def agent_logs_page(request: Request):
    """Agent logs page"""
    return templates.TemplateResponse("agentlogs.html", {"request": request})


@router.get("/commandlogs", response_class=HTMLResponse)
async def command_logs_page(request: Request):
    """Command logs page"""
    return templates.TemplateResponse("commandlogs.html", {"request": request})


@router.get("/soaplogs", response_class=HTMLResponse)
async def soap_logs_page(request: Request):
    """SOAP logs page"""
    return templates.TemplateResponse("soaplogs.html", {"request": request}) 