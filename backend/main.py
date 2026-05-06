from fastapi import FastAPI #FastAPIライブラリからAPIをつくるための部品を取り込む
from pydantic import BaseModel #受け取るデータの方を定義するための部品を取り込む

app = FastAPI() #APIアプリの本体をつくる

class InquiryRequest(BaseModel):
    question: str #question という名前の文字列データを受け取る

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    return {
        "category": "その他",
        "priority": "低",
        "answer": f"問い合わせ内容を受け付けました: {request.question}"
    }