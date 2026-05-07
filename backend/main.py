#バックエンド起動方法：uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

from fastapi import FastAPI #FastAPIライブラリからAPIをつくるための部品を取り込む
from pydantic import BaseModel #受け取るデータの方を定義するための部品を取り込む
from backend.storage import save_inquiry, load_inquiries

app = FastAPI() #APIアプリの本体をつくる

class InquiryRequest(BaseModel):
    question: str #question という名前の文字列データを受け取る

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    item = save_inquiry(
        question = request.question,
        category = "その他",
        priority = "中",
        answer = "問い合わせ内容を受け付けました。"
    )
    return item

@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()