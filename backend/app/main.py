from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.chat import router as chat_router


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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
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