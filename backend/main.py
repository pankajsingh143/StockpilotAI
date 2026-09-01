from fastapi import FastAPI
from backend.api.health import health_router    

app = FastAPI(
    title="Stock Pilot API",
    version="0.1.0",
    description="An API for Stock Pilot, a stock market analysis tool."        
)

@app.get("/")
def home():
    return {
        "application": "Stock Pilot API",
        "version": "0.1.0",
        "description": "An API for Stock Pilot, a stock market analysis tool."
    }

app.include_router(health_router)