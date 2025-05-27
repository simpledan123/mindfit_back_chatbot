from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ 추가
from fastapi.staticfiles import StaticFiles
from api.v1.routers import router as api_router

app = FastAPI()

# ✅ CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 프론트엔드에서 접근 허용 (운영 시엔 도메인 제한 권장)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.mount("/images", StaticFiles(directory="static/review_images"), name="images")
