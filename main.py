import streamlit as st
import pandas as pd
import datetime

# https://ourworldindata.org/coronavirus-source-data

countries = ["JPN", "FRA", "USA", "GBR", "DEU",
             "ITA", "CAN", "RUS", "CHN", "KOR", "VNM"]

cols = ["iso_code", "date", "new_cases", "new_deaths", "new_tests"]

# データを読込
@st.cache
def load_df():
    df = pd.read_csv("owid-covid-data.csv")
    df = df[cols]
    df = df[df["iso_code"].isin(countries)]
    df["date"] = pd.to_datetime(df['date'])
    df = df.set_index(["date"])
    return df


# 日付セレクターを作成
selected_from = st.sidebar.date_input(
    "開始日", datetime.datetime.strptime("2020-04-01", "%Y-%m-%d"))
selected_to = st.sidebar.date_input("終了日", datetime.date.today())

# 国セレクターを作成
selected_country = st.sidebar.selectbox("国", countries)

# セレクターに応じてデータを編集
df = load_df()
df = df[df["iso_code"] == selected_country]
df = df.drop("iso_code", axis=1)
df = df.query("@selected_from <= date <= @selected_to")

# カラムセレクターを作成
selected_cols = st.sidebar.multiselect("グラフを表示するデータ", df.columns)

# グラフなどを描画
f"""
# {selected_country}の日別推移グラフ
> 期間：{selected_from} ~ {selected_to}
"""
for c in selected_cols:
    st.bar_chart(df[c])
    f"""
    ---
    """
