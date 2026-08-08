from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.chat import router as chat_router
from app.config import settings


app = FastAPI(
    title="NUTU API",
    description="Backend API for NUTU Personal AI Assistant",
    version="1.0.0"
)


# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://([a-z0-9-]+\.)?vercel\.app",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# Chat Router
# -----------------------------------------

app.include_router(chat_router)


# -----------------------------------------
# Static Files
# Resume PDF
# -----------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# -----------------------------------------
# Root
# -----------------------------------------

@app.get("/")
def root():
    return {
        "message": "NUTU API is running"
    }
