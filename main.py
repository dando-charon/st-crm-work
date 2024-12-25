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
    "customer/dashboard.py",
    title="ダッシュボード",
    icon=":material/dashboard:",
    default=True,
)
contracts = st.Page(
    "customer/contracts.py", title="契約", icon=":material/bug_report:"
)
company = st.Page("customer/company.py", title="取引先企業", icon="✨")

activity = st.Page("sales/activity.py", title="活動報告", icon=":material/search:")
history = st.Page("sales/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Customer": [dashboard, contracts, company],
            "Sales": [activity, history],
        }
    )
else:
    pg = st.navigation([login_page])


pg.run()
