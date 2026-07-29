from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.chat import router as chat_router


app = FastAPI(
    title="NUTU API",
    description="Personal AI Assistant for Mohammed Yassin",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to NUTU API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NUTU Backend"
    }