from fastapi import APIRouter
from src.endpoints import attachment
from src.endpoints import database_management
from src.endpoints import register
from src.endpoints import user

router = APIRouter()
#
router.include_router(attachment.router)
router.include_router(database_management.router)
router.include_router(register.router)
router.include_router(user.router)

