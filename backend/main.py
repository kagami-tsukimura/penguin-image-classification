from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
