# バックエンド起動方法：uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

from fastapi import FastAPI # FastAPIライブラリからAPIをつくるための部品を取り込む
from pydantic import BaseModel # 受け取るデータの方を定義
from backend.storage import save_inquiry, load_inquiries # strage.pyに記載の関数

import os #環境変数を読みこむ
from dotenv import load_dotenv #.env ファイルから環境変数を読み込む
from google import genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) #genai.Client→ GeminiAPIと通信するためのクライアントを作成
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite") #使用するモデルを環境変数から読み込む。環境変数に設定がない場合は "gemini-2.5-flash-lite" を使う


app = FastAPI() #APIアプリの本体をつくる


class InquiryRequest(BaseModel):
    question: str # /analyzeに送られてくるJSONの型を定義。questionという名前の文字列データを受け取る。


def analyze_with_gemini(question: str) -> str: #「question: str」  → 引数は「問い合わせ内容（文字列）」「-> str」 → 戻り値は「AI の返答（文字列）」
    prompt = f"""
あなたは総務部門の問い合わせ一次回答担当です。
社員からの問い合わせを読み、以下の3点を日本語で返してください。

1. カテゴリ
2. 緊急度（高・中・低）
3. 回答案

問い合わせ:
{question}
"""
    response = client.models.generate_content( #Gemini に「このプロンプトで回答して」と依頼する
        model=MODEL, #使うモデルを指定
        contents=prompt #AI に渡す文章
    )
    return response.text #Geminiの回答がresponse.textに入るので、FastAPIに返す



@app.get("/") 
    #GETは情報を取りに行く。URL"http://127.0.0.1:800/"にアクセスされたら実行してねとFastAPIに教える
def root():  #動作確認用。APIがちゃんと動いているか確認する。
    return {"message": "API is running!"}



@app.post("/analyze") 
    #POSTはデータをもっていく。URL"http://127.0.0.1:8000/analyze"にPOSTリクエストが来たら実行してねとFastAPIに教える
    #大意は、FastAPIがPOSTで送られてきた問い合わせ（question）を受け取り、JSON に保存する
def analyze_inquiry(request: InquiryRequest):
            #requestはInquiryRequest型→request.questionはstring型
    ai_result = analyze_with_gemini(request.question) #AIに問い合わせ内容を渡して、AIの回答をもらう
    item = save_inquiry(   #storage.py内。問い合わせ内容を保存する
        question = request.question,    #JSONの"question"がPythonのrequest.questionniに変換された
        category = "その他",
        priority = "中",
        answer = ai_result
    )
    return item #保存した内容をフロントエンドに返す



@app.get("/inquiries") 
    #URL"http://127.0.0.1:8000/inquiries"にGETリクエストが来たら実行してねとFastAPIに教える
def get_inquiries():  #JSONファイルに保存された全問い合わせ一覧を返す
    return load_inquiries() #問い合わせのリストをフロントエンドに返す