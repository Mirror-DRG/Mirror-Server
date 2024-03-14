from fastapi import APIRouter, File, HTTPException
from PIL import Image
from transformers import pipeline
import io


router = APIRouter(
    prefix="/captioning",
    tags=["Image Captioning"]
)

@router.post("")
async def receive_image(file: bytes = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    caption = image_captioning(file)

    return caption

async def image_captioning(img):
    img = Image.open(io.BytesIO(img))
    if img.mode != "RGB":
        img = img.convert("RGB")

    image_to_text = pipeline("image-to-text", model="./model")

    return image_to_text(img)[0]["generated_text"]


@router.get("/test")
async def root():
    return {"message": "router test"}