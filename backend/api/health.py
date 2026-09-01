from fastapi import APIRouter

health_router = APIRouter()

@health_router.get("/health")
def health():
    return {"status": "UP", "message": "The Stock Pilot API is running smoothly."}
