import streamlit as st
import pandas as pd
from datetime import datetime

# サンプルデータの作成（10件）
data = {
    '案件名': ['New York', 'London', 'Tokyo', 'Paris', 'Berlin', 'Sydney', 'Moscow', 'Amsterdam', 'Dubai', 'Rome'],
    '案件開始日': ['2024-' + f'{i%12+1:02d}' + '-01' for i in range(5)] + ['2023-' + f'{i%12+1:02d}' + '-01' for i in range(5)],
    'クライアント企業名': [f'企業{i%5}' for i in range(1, 11)],
    'クライアント側担当者名': [f'担当者{i%5}' for i in range(1, 11)],
    '部署別': [f'部署{i%5}' for i in range(1, 11)],
    '担当者': [f'担当者{i%4}' for i in range(1, 11)],
    '契約スタート日': ['2024-01-01', '2024-02-01', '', '2024-03-01', '', '2024-04-01', '', 
                   '2024-05-01', '', '2024-06-01'],
    '契約終了日': ['2024-12-31', '2024-11-30', '', 
                   '2024-10-31', '', 
                   '2024-09-30', '', 
                   '2024-08-31', '', 
                   '2024-07-31'],
    "確度": [chr(65 + i % 6) for i in range(10)]  # AからFまでのランク
}

details_data = {
    "案件名": ['New York', 'London', 'Tokyo', 'Paris', 'Berlin', 'Sydney', 'Moscow',
               "Amsterdam", "Dubai", "Rome"],
    "クライアント企業名": [f'企業{i%5}' for i in range(1, 11)],
    "報酬金額": [1000000 * (i+1) for i in range(1, 11)],
    "契約締結確度": [chr(65 + i % 6) for i in range(1, 11)],  # AからFまでのランク
    "メモ": [f'brabrabrabrabra vidi vini vici{i} brabrabrabrabra  brabr123123123abrabrabra  brabrabrabrabra hogehogehogeho' for i in range(1, 11)]
}

df = pd.DataFrame(data)
details_df = pd.DataFrame(details_data)

# 年月の選択肢を作成
years = list(range(2023, 2026))
months = list(range(1, 13))

# フィルターの作成
st.header('フィルター')
col1, col2 = st.columns([1, 2])
with col1:
    selected_department = st.multiselect('部署別', df['部署別'].unique())
    selected_person = st.multiselect('担当者', df['担当者'].unique())
    selected_company = st.multiselect('企業別', df['クライアント企業名'].unique())
with col2:
    selected_year = st.selectbox('年を選択してください。:', [None] + years)
    selected_month = st.selectbox('月を選択してください。:', [None] + months)
    
    # 選択解除ボタン
    if st.button('選択を解除する'):
        selected_year = None
        selected_month = None

# フィルターの適用
if selected_department:
    df = df[df['部署別'].isin(selected_department)]
if selected_person:
    df = df[df['担当者'].isin(selected_person)]
if selected_company:
    df = df[df['クライアント企業名'].isin(selected_company)]
if selected_year and selected_month:
    start_date_str = f"{selected_year}-{selected_month:02d}-01"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    df['案件開始日'] = pd.to_datetime(df['案件開始日'], errors='coerce')
    df = df[(df['案件開始日'].dt.year == start_date.year) & (df['案件開始日'].dt.month == start_date.month) | df['案件開始日'].isna()]

# 案件リストの表示
st.write('## 案件リスト')
st.dataframe(df)

# 案件名をクリックすると詳細データを表示
st.write('## 案件詳細')
selected_project = st.selectbox('案件名を選択してください。:', options=[''] + df['案件名'].tolist(), key='project_selectbox')
if selected_project:
    project_details = details_df[details_df['案件名'] == selected_project].iloc[0]
    
    # カード形式で表示
    with st.container():
        with st.container(border=True):
            left, middle, right = st.columns(3)
            
            left.metric(label="案件名", value=str(project_details['案件名']))
            middle.metric(label="クライアント企業名", value=str(project_details['クライアント企業名']))
            right.metric(label="報酬金額", value=f"¥{project_details['報酬金額']:,}")
            
            left.metric(label="契約締結確度", value=str(project_details['契約締結確度']))
        
        # メモを画面幅いっぱいに細長く表示
        with st.container(border=True):
            st.markdown(f"**メモ:**  \n \n {project_details['メモ']}", unsafe_allow_html=True)

