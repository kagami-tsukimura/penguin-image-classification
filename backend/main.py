from fastapi import FastAPI

app = FastAPI()


# 起動確認
@app.get("/")
async def root():
    return {"message": "Welcome to Penguin-classification API!"}
