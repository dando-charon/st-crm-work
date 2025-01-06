import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "views/customer/dashboard.py",
    title="ダッシュボード",
    icon=":material/dashboard:"
)
contracts = st.Page(
    "views/customer/contracts.py", title="契約", icon="💼"
)
company = st.Page("views/customer/company.py", title="取引先企業", icon="📕")

activity = st.Page("views/sales/activity.py", title="活動報告", icon="📰")
case = st.Page("views/sales/case.py", title="案件", icon="🎁")
assign = st.Page("views/sales/assign.py", title="アサイン情報", icon="🚩")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "アカウント": [logout_page],
            "顧客": [dashboard, contracts, company],
            "営業": [activity, case, assign],
        }
    )
else:
    pg = st.navigation([login_page])


pg.run()


# 手順: 

# CRMダッシュボードにアクセス。 

# 「行動管理」セクションを選択。 

# 集計したい期間（例：今月、四半期）を設定。 

# 集計基準として「企業（もしくは企業グループ）」、「担当者（重要人物）」を選択。 

# 集計基準に基づいて、案件リスト、活動報告の一覧表示させることができる。 

# 案件リストにはフィルター機能があり、部署別、担当者別、期間別で抽出することができる。 

# それぞれの案件に関してはクリックで詳細を表示することができる。 

# 集計結果をエクスポートして、チームミーティングで共有。 