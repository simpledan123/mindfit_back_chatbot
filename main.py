from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1.routers import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
app.mount("/images", StaticFiles(directory="static/review_images"), name="images")
