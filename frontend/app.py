#起動方法: uv run streamlit run frontend/app.py

import streamlit as st
import pandas as pd
import time
import requests

def wait(seconds :int): #秒数を受け取って、秒数間プログレスバーを表示しながら待つ関数
    progress = st.progress(0)
    status = st.empty()
    for i in range(seconds):
        progress.progress((i + 1) / seconds)
        status.text(f"{i + 1}秒経過...")
        time.sleep(1)
    status.write("完了！")


st.sidebar.title("メニュー")
st.sidebar.write("問い合わせを入力するか、過去の問い合わせ履歴を閲覧しましょう。")
page = st.sidebar.selectbox("ページ", ["問い合わせ入力","履歴一覧"])

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

        if st.form_submit_button("送信"):
            if question.strip() == "":
                st.error("問い合わせ内容を入力してください")
            else :
                response = requests.post(
                    "http://127.0.1:8000/analyze",
                    json={"question": question},
                    timeout = 30
                )
                result = response.json()
                st.write("カテゴリ:", result["category"])
                st.write("緊急度:", result["priority"])
                st.write("回答案:", result["answer"])
        #260505
        #if st.form_submit_button("送信"):
        #    if question.strip() == "" and name.strip() == "":
        #        st.error("名前と問い合わせ内容を入力してください")
        #    elif question.strip() == "" and name.strip() != "":
        #        st.error("問い合わせ内容を入力してください")
        #    elif question.strip() != "" and name.strip() == "":
        #        st.error("名前を入力してください")
        #    elif not agree:
        #        st.error("内容に同意してださい")
        #    else:
        #        with st.spinner("送信中..."):
        #            wait(3)
        #            st.success(f"{name}様の問い合わせが送信されました")

if page == "履歴一覧":

    st.title ("履歴一覧")
    st.write("過去の問い合わせ履歴を閲覧できます")

    inquiries = [
        {"受付番号": 1, "名前": "大谷翔平", "問い合わせ内容": "休暇の申請方法を教えてください", "カテゴリ": "休暇", "日付": "2024-06-01"},
        {"受付番号": 2, "名前": "山本由伸", "問い合わせ内容": "福利厚生のシステムについてしりたいです", "カテゴリ": "福利厚生", "日付": "2024-06-03"}
    ]
    st.table(pd.DataFrame(inquiries))