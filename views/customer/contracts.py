import streamlit as st
import pandas as pd
# import openpyxl
import warnings

st.title("契約")

 # エクセルファイルを読み込み
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    df = pd.read_excel('./test/data/contracts.xlsx', engine='openpyxl')
    
# データフレームを表示

st.dataframe(df)