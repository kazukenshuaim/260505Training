# バックエンド起動方法：uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

from fastapi import FastAPI # FastAPIライブラリからAPIをつくるための部品を取り込む
from pydantic import BaseModel # 受け取るデータの方を定義
from backend.storage import save_inquiry, load_inquiries # strage.pyに記載の関数

app = FastAPI() #APIアプリの本体をつくる

class InquiryRequest(BaseModel):
    question: str # /analyzeに送られてくるJSONの型を定義。questionという名前の文字列データを受け取る。

@app.get("/") 
    #GETは情報を取りに行く。URL"http://127.0.0.1:800/"にアクセスされたら実行してねとFastAPIに教える
def root():  #動作確認用。APIがちゃんと動いているか確認する。
    return {"message": "API is running!"}

@app.post("/analyze") 
    #POSTはデータをもっていく。URL"http://127.0.0.1:8000/analyze"にPOSTリクエストが来たら実行してねとFastAPIに教える
    #大意は、FastAPIがPOSTで送られてきた問い合わせ（question）を受け取り、JSON に保存する
def analyze_inquiry(request: InquiryRequest):
            #requestはInquiryRequest型→request.questionはstring型
    item = save_inquiry(   #storage.py内。問い合わせ内容を保存する
        question = request.question,    #JSONの"question"がPythonのrequest.questionniに変換された
        category = "その他",
        priority = "中",
        answer = "問い合わせ内容を受け付けました。"
    )
    return item #保存した内容をフロントエンドに返す

@app.get("/inquiries") 
    #URL"http://127.0.0.1:8000/inquiries"にGETリクエストが来たら実行してねとFastAPIに教える
def get_inquiries():  #JSONファイルに保存された全問い合わせ一覧を返す
    return load_inquiries() #問い合わせのリストをフロントエンドに返す