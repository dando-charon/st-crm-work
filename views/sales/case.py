import streamlit as st
import pandas as pd
import warnings
st.write("案件")


 # エクセルファイルを読み込み
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    df = pd.read_csv('./test/data/supermarket_sales.csv',index_col=0)
    
# データフレームを表示

st.dataframe(df)