from fastapi import APIRouter

from .historical_ciphers import router as historical_router

router = APIRouter(prefix="/api")
router.include_router(historical_router)