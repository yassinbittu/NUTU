from fastapi import FastAPI

app = FastAPI(
    title="NUTU API",
    description="Personal AI Assistant for Mohammed Yassin.",
    version="1.0.0",
)


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