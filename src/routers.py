from fastapi.routing import APIRouter

from router import login_router, user_router

router = APIRouter(prefix="/api")
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(login_router, prefix="/auth", tags=["auth"])
