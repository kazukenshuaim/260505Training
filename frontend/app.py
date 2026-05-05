import streamlit as st
import pandas as pd


import pandas as pd

st.title("総務問い合わせフォーム")
st.write("社員から総務への問い合わせを入力してください。")

with st.form("inquiry_form"):
    name = st.text_input("氏名")
    question = st.text_area("問い合わせ内容", height=160)
    priority = st.radio("緊急度", ["High", "Middle", "Low"])
    category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
    submitted = st.form_submit_button("送信する")

if submitted:
    if question.strip() == "" or name.strip() == "":
        st.error("すべてのフィールドを入力してください。")
    else:
        st.success(f"{name}さんの問い合わせを受け付けました。回答をお待ちください。")
