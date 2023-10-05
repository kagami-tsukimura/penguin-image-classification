import io

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model.model_eval import (
    eval_cnn,
    is_production,
    judge_pred,
    load_model,
    prepare_data,
)
from PIL import Image, ImageFile

app = FastAPI()

if is_production():
    MODEL = "./model/mobilenet-penguin-7cls.pt"
else:
    MODEL = "./model/efficientnet-penguin-7cls.pt"

device, model = load_model(MODEL)

# CORSミドルウェアを有効にする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 起動確認
@app.get("/")
async def root():
    return {"message": "Welcome to Penguin-classification API!"}


# 画像分類
@app.post("/classify/")
async def classify_image(file: UploadFile):
    try:
        # NOTE: Make sure you can read large sized images.
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img_data = await file.read()
        img = Image.open(io.BytesIO(img_data)).convert("RGB")

        test_transform = prepare_data()
        pred = eval_cnn(img, test_transform, model, device)
        dst = judge_pred(pred)

        return JSONResponse(content={"id": pred, "name": dst})

    except Exception as e:
        return JSONResponse(content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app)
