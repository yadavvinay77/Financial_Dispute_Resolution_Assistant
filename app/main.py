# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.upload import router as upload_router
from app.api.ask import router as ask_router
from app.api.ask_stream import router as ask_stream_router
from app.api.ingest_text import router as ingest_text_router

app = FastAPI()

# Register routers
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(ask_stream_router)
app.include_router(ingest_text_router)

# Correct folder paths (IMPORTANT FIX)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
