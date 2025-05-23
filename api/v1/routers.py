from .endpoints import chatbot
from fastapi import APIRouter
from api.v1.endpoints import restaurants, reviews, users, auth, bookmarks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])  # ✅ 추가됨

router = api_router  # 외부에서 import 가능하게 alias 추가
