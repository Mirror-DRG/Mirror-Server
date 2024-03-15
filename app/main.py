from fastapi import FastAPI
import uvicorn
from routers import ImageCaptioning

app = FastAPI()
app.include_router(ImageCaptioning.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info"
                , ssl_keyfile="C:\Windows\System32\key.pem"
                , ssl_certfile="C:\Windows\System32\cert.pem")
