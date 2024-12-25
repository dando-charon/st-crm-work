import streamlit as st
import pandas as pd
# import openpyxl
import warnings

st.title("contracts")

 # エクセルファイルを読み込み
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    df = pd.read_excel('./data/contracts.xlsx', engine='openpyxl')
    
# データフレームを表示
st.write('アップロードされたデータ:')
st.dataframe(df)