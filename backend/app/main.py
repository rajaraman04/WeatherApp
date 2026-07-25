from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Weather App", description=("A simple weather app API for weather retrieval and CRUD operations"), version="1.0.0")
allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173",]

app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False, allow_methods=["GET", "POST", "PUT", "DELETE","OPTIONS"], allow_headers=["content-type", "Authorization"])
@app.get("/",tags=["General"])
async def root():
    return {"message": "Welcome to the Weather App API!",
            "documentation":"/docs",}

@app.get("/api/health",tags=["General"])
async def health_check():
    return {"status": "healthy",
            "service": "Weather App API",
            "version": "1.0.0",}