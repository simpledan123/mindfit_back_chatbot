from typing import List
import uuid
import os
from io import BytesIO
from fastapi import UploadFile
from sqlalchemy.orm import Session
from PIL import Image as PILImage
from models.user import User
from models.review import Review
from models.image import Image

UPLOAD_DIR = "static/review_images"

def upload_images(db: Session, current_user: User, review_id: int, files: List[UploadFile]):    
    review = db.query(Review).filter(Review.id == review_id).first()
    
    for file in files:
        filename = uuid.uuid4().hex
        save_review_image(filename, file)
        image = Image(filename=filename, review_id=review.id)
        db.add(image)

    db.commit()

def save_review_image(filename: str, file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise ValueError("지원하지 않는 이미지 형식입니다.")

    contents = file.file.read()
    image = PILImage.open(BytesIO(contents)).convert("RGB")

    image = resize_image(image, max_size=2048)
    original_path = os.path.join(UPLOAD_DIR, "original", f"{filename}.webp")
    image.save(original_path, "webp", quality=85)

    save_thumbnail(image, filename, size=300)
    save_thumbnail(image, filename, size=750)


def resize_image(image: PILImage.Image, max_size: int = 2048) -> PILImage.Image:
    width, height = image.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        return image.resize((int(width * ratio), int(height * ratio)), PILImage.LANCZOS)
    return image


def save_thumbnail(image: PILImage.Image, filename: str, size: int):
    croped = crop_center_square(image)
    thumb = resize_image(croped, size)
    thumb_dir = os.path.join(UPLOAD_DIR, f"thumb_{size}")
    os.makedirs(thumb_dir, exist_ok=True)

    basename = os.path.splitext(filename)[0]
    thumb_filename = f"{size}_{size}_{basename}.webp"
    thumb_path = os.path.join(thumb_dir, thumb_filename)

    thumb.save(thumb_path, format="WEBP", quality=85)


def crop_center_square(image: PILImage.Image) -> PILImage.Image:
    width, height = image.size
    min_dim = min(width, height)

    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    return image.crop((left, top, right, bottom))


