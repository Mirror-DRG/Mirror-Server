from fastapi import APIRouter, File, HTTPException, UploadFile

# 번역 관련
from googletrans import Translator
import httpx

# model 관련 import
from PIL import Image
from transformers import pipeline
import io

router = APIRouter(
    prefix="/captioning",
    tags=["Image Captioning"]
)
# google
translator = Translator()
# naver papago
clientID = "clientID"
clientSecret = "clientSecret"

@router.post("")
async def receive_image(image: UploadFile = File(...)):
     # filename exception
     if image.filename.split(".")[-1] not in ["jpg", "jpeg"]:
        print("not jpg or jpeg") # raise exception 
     
     if not image:
        raise HTTPException(status_code=400, detail="No file provided")

     image_byte = await image.read()
     caption = image_captioning(image_byte)
     print(caption)

     # google translation
     translation_caption = translator.translate(caption, dest='ko').text

     # papago translation
     # async with httpx.AsyncClient() as client:
     #     response = await client.post(
     #         "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation",
     #         headers={
     #             "X-NCP-APIGW-API-KEY-ID": clientID,
     #             "X-NCP-APIGW-API-KEY": clientSecret
     #         },
     #         json={"source": "en", "target": "ko", "text": caption},
     #     )
     # translation_caption = response.json()["message"]["result"]["translatedText"]

     return translation_caption


def image_captioning(img):
    img = Image.open(io.BytesIO(img))
    if img.mode != "RGB":
        img = img.convert("RGB")

    image_to_text = pipeline("image-to-text", model="./model")

    return image_to_text(img)[0]["generated_text"]


@router.get("/test")
async def root():
    return {"message": "router test"}
