from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.config import settings
from src.routes import shortener, stats, health, redirect


app = FastAPI(
    title=settings.app_name,
    description="Fast URL shortener with metrics",
    version="0.0.1",
    debug=settings.debug,
    redirect_slashes=True,
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Templates
templates = Jinja2Templates(directory="src/web/templates")

# Web page routes (must be defined before API routes)
@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stats", response_class=HTMLResponse)
async def stats_interface(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})


@app.get("/links", response_class=HTMLResponse)
async def links_interface(request: Request):
    return templates.TemplateResponse("links.html", {"request": request})

# API routes
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(stats.router)
api_router.include_router(shortener.router)

app.include_router(api_router)
app.include_router(redirect.router)
