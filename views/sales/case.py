import streamlit as st
import pandas as pd
from streamlit_card import card

# サンプルデータの作成（20件）
data = {
    '案件名': [f'案件{i}' for i in range(1, 21)],
    'クライアント企業名': [f'企業{i%5}' for i in range(1, 21)],
    'クライアント側担当者名': [f'担当者{i%5}' for i in range(1, 21)],
    '部署別': [f'部署{i%5}' for i in range(1, 21)],
    '担当者': [f'担当者{i%4}' for i in range(1, 21)],
    '契約スタート日': ['2024-01-01', '2024-02-01', '', '2024-03-01', '', '2024-04-01', '', '2024-05-01', '', '2024-06-01', '', '2024-07-01', '', '2024-08-01', '', '2024-09-01', '', '2024-10-01', '', '2024-11-01'],
    '契約終了日': ['2024-12-31', '2024-11-30', '', '2024-10-31', '', '2024-09-30', '', '2024-08-31', '', '2024-07-31', '', '2024-06-30', '', '2024-05-31', '', '2024-04-30', '', '2024-03-31', '', '2024-02-28'],
    '確度': [chr(65 + i % 6) for i in range(20)]  # AからFまでのランク
}

details_data = {
    '案件名': [f'案件{i}' for i in range(1, 21)],
    'クライアント企業名': [f'企業{i%5}' for i in range(1, 21)],
    '報酬金額': [1000000 * (i+1) for i in range(20)],
    '契約締結確度': [chr(65 + i % 6) for i in range(20)],  # AからFまでのランク
    'メモ': [f'brabrabrabrabra vidi vini vici{i}' for i in range(1, 21)]
}

df = pd.DataFrame(data)
details_df = pd.DataFrame(details_data)

# フィルターの作成
st.header('フィルター')
col1, col2, col3 = st.columns(3)
with col1:
    selected_department = st.multiselect('部署別', df['部署別'].unique())
with col2:
    selected_person = st.multiselect('担当者', df['担当者'].unique())
with col3:
    selected_period = st.date_input('期間', [])

# フィルターの適用
if selected_department:
    df = df[df['部署別'].isin(selected_department)]
if selected_person:
    df = df[df['担当者'].isin(selected_person)]
if selected_period:
    if len(selected_period) == 2:
        start_date, end_date = selected_period
        df = df[(df['契約スタート日'] >= str(start_date)) & (df['契約終了日'] <= str(end_date))]
    else:
        st.warning('日付を指定してください。')

# 案件リストの表示
st.write('## 案件リスト')
st.dataframe(df)

# 案件名をクリックすると詳細データを表示
st.write('## 案件詳細')
selected_project = st.selectbox('案件名を選択', df['案件名'])
if selected_project:
    project_details = details_df[details_df['案件名'] == selected_project]
    
    # カード形式で表示
    st.markdown(
        """
        <style>
        .card {
            background-color: #e0f7e0;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    with st.container(border=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cols = st.columns(2)
        cols[0].markdown(f"**案件名:** {project_details['案件名'].values[0]}")
        cols[1].markdown(f"**クライアント企業名:** {project_details['クライアント企業名'].values[0]}")
        
        cols = st.columns(2)
        cols[0].markdown(f"**報酬金額:** ¥{project_details['報酬金額'].values[0]:,}")
        cols[1].markdown(f"**契約締結確度:** {project_details['契約締結確度'].values[0]}")
        
        st.markdown(f"**メモ:** {project_details['メモ'].values[0]}")
        st.markdown('</div>', unsafe_allow_html=True)