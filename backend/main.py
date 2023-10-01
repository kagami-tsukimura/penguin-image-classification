import io

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model.model_eval import load_model
from PIL import Image

app = FastAPI()

MODEL = "./model/efficientnet-penguin-7cls.pt"
model = load_model(MODEL)

# CORSミドルウェアを有効にする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンからのリクエストを許可（開発用途）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 起動確認
@app.get("/")
async def root():
    return {"message": "Welcome to Penguin-classification API!"}


@app.post("/classify/")
async def classify_image(file: UploadFile):
    try:
        img_data = await file.read()
        img = Image.open(io.BytesIO(img_data))

        result = predict_image(img)

        return JSONResponse(content={"result": result})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
