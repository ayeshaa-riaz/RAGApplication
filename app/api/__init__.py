from fastapi import APIRouter
from .auth import router as auth_router
from .chat import router as chat_router
from .sources import router as sources_router
from .users import router as users_router

# Create API router with prefix
api_router = APIRouter(prefix="/api")

# # Include all routers with their specific prefixes
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(sources_router, prefix="/sources", tags=["sources"])

