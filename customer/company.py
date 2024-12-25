import streamlit as st
import pandas as pd
import sqlite3

# st.set_page_config(
#     page_title="取引先企業",
#     page_icon=":sparkles:"
# )

# サンプルデータの作成
# data = {
#     '会社CD': ['230948', '54098', '988'],
#     'TickerCD': ['3090', '2335', '39875'],
#     '会社名': ['フロンティアマネジメント株式会社', '三井不動産', '株式会社ABC']
# }

# SQLiteデータベースに接続
conn = sqlite3.connect('./data/accounts.db')

# SQLクエリを実行してデータを取得
query = "SELECT * FROM accounts"
df = pd.read_sql_query(query, conn)

# データベース接続を閉じる
conn.close()

# 必要なカラムだけをピックアップ
df = df[['name',
         'san_org_registration_addressinside',
         'san_org_registration_addressinside_prefecture', 
         'san_org_registration_addressinside_zipcode',
         'san_org_tdb_kanatradenameforsearch',
         'san_org_registration_addressinside_city']]

# カラム名を変更
df = df.rename(columns={'san_org_registration_addressinside_prefecture': '所在地（県）', 
    'san_org_registration_addressinside_city': '所在地（市町村）',
                        'san_org_registration_addressinside_zipcode': '郵便番号',
                        'san_org_registration_addressinside': '所在地',
                        'san_org_tdb_kanatradenameforsearch':'カナ',
                        'name': '企業名'})

# Streamlitでテーブルを表示
# st.title(':sparkles: 取引先企業 ')
# 検索ボックスを作成してページタイトルの下に表示
search_term = st.text_input('検索', '')

# 検索ボックスの入力に基づいてデータフレームをフィルタリング
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
st.dataframe(df,  use_container_width=True, hide_index=False)

