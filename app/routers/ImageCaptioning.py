from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image
from transformers import pipeline
import io

router = APIRouter(
    prefix="/captioning",
    tags=["Image Captioning"]
)

#@router.post("")
#async def receive_image(image: bytes = File(...)):
#    if not image:
#        raise HTTPException(status_code=400, detail="No file provided")
#
#     print(image)
#    caption = image_captioning(image)
#
#    return caption

@router.post("")
async def receive_image(image: UploadFile = File(...)):
     # filename, exception?
     if image.filename.split(".")[-1] not in ["jpg", "jpeg"]:
        print("not jpg or jpeg") # raise exception 
     
     if not image:
        raise HTTPException(status_code=400, detail="No file provided")

     image_byte = await image.read()
     caption = image_captioning(image_byte)

     return caption

#@router.post("/test")
#async def receive_image(reqBody: dict = None):
#    print(reqBody) # dict type error

def image_captioning(img):
    img = Image.open(io.BytesIO(img))
    if img.mode != "RGB":
        img = img.convert("RGB")

    image_to_text = pipeline("image-to-text", model="./model")

    return image_to_text(img)[0]["generated_text"]


@router.get("/test")
async def root():
    return {"message": "router test"}
