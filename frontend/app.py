#フロントエンド起動方法: uv run streamlit run frontend/app.py

import streamlit as st
import pandas as pd
import time
import requests


st.sidebar.title("メニュー")
st.sidebar.write("問い合わせを入力するか、過去の問い合わせ履歴を閲覧しましょう。")
page = st.sidebar.radio("ページ", ["問い合わせ入力","履歴一覧"])

if page == "問い合わせ入力": #サイドバーで「問い合わせ入力」が選択されたときの画面を作る

    st.title("問い合わせ入力")
    st.write("社員から総務への問い合わせを入力してください。")
    st.markdown("**注**: 問い合わせ内容はできる限り具体的にするようお願いいたします。")
    with st.form("inquiry_form"): #入力欄が複数ある時、すべて入力してからまとめて送信
        name = st.text_input("名前")
        id = st.number_input("社員ID", min_value=1, max_value=9999, step=1)
        question = st.text_area("問い合わせ内容", height = 160)
        category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
        agree = st.checkbox("内容を確認しました")
        
        if st.form_submit_button("APIに送信"):
            if question.strip() == "" and name.strip() == "":
                st.error("名前と問い合わせ内容を入力してください")
            elif question.strip() == "" and name.strip() != "":
                st.error("問い合わせ内容を入力してください")
            elif question.strip() != "" and name.strip() == "":
                st.error("名前を入力してください")
            elif not agree:
                st.error("内容に同意してださい")
            else :
                response = requests.post( 
                    #大意は、"/analyze"に{"question": question}を送る
                    #バックエンドにデータを送るためにHTTPPOSTリクエストを送る
                    "http://127.0.0.1:8000/analyze", #FastAPI の analyze_inquiry 関数を呼びに行っている
                    json={"question": question}, 
                        #POSTリクエストの中身。フォームで入力された内容(question)をJSON形式でサーバーに送る
                        #json= → 「サーバ（バックエンド）に送るデータはこれですよ」と指定する部分
                        #"question" → JSON のキー（項目の名前）
                        #question → Python 変数（ユーザーが入力した文字）
                        #バックエンド側では request: InquiryRequest型オブジェクト として受け取り、request.question で取り出している
                    timeout = 30
                )
                result = response.json() 
                    # バックエンドから返ってきたJSONをPythonのdict に変換
                    # → バックエンドの save_inquiry() が返した item がここに入る
                st.write("カテゴリ:", result["category"])
                st.write("緊急度:", result["priority"])
                st.write("回答案:", result["answer"])
                    #result["~~~"]はバックエンドで保存した値

if page == "履歴一覧":

    st.subheader("問い合わせ一覧")
    resp = requests.get("http://127.0.0.1:8000/inquiries", timeout=10)
        #@app.get("/inquiries") にアクセスし、全問い合わせを取りに行く
    if resp.status_code == 200: #HTTP ステータスコード 200 は「成功」
        inquiries = resp.json() #バックエンドから返ってきた JSON（問い合わせ一覧）を Python のリストに変換
        if inquiries: #リストが空じゃなければ、True
            for item in inquiries:  #問い合わせ一覧から1件ずつ取り出して、画面に表示
                st.write(f"[{item['id']}] {item['created_at']} | {item['question'][:40]}")
                # item['id']  
                # → JSON 保存時に付けた連番 ID
                # item['created_at']  
                # → 保存した日時（datetime.now().strftime(...) の結果）
                # item['question'][:40]  
                # → 問い合わせ内容の先頭40文字だけを表示
                # → 長すぎる文章を一覧で全部出さないための工夫
        else:
            st.write("まだ問い合わせはありません。")