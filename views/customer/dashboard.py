import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Generate sample sales data for departments with more variability
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365)
sales_data = pd.DataFrame({
    'Department A': np.random.randint(50, 1500, size=365) * np.random.choice([1, 1.5, 2], size=365),
    'Department B': np.random.randint(50, 1500, size=365) * np.random.choice([1, 1.5, 2], size=365),
    'Department C': np.random.randint(50, 1500, size=365) * np.random.choice([1, 1.5, 2], size=365)
}, index=dates)

# Generate sample sales target data for departments
sales_target_data = pd.DataFrame({
    'Department A': np.random.randint(100, 1200, size=365) * np.random.choice([1, 1.5, 2], size=365),
    'Department B': np.random.randint(100, 1200, size=365) * np.random.choice([1, 1.5, 2], size=365),
    'Department C': np.random.randint(100, 1200, size=365) * np.random.choice([1, 1.5, 2], size=365)
}, index=dates)

# Add quarter column to sales data and sales target data
sales_data['Quarter'] = sales_data.index.to_period('Q')
sales_target_data['Quarter'] = sales_target_data.index.to_period('Q')

# Resample sales data and sales target data to monthly and quarterly frequency
monthly_sales_data = sales_data.resample('MS').sum(numeric_only=True).reset_index()
quarterly_sales_data = sales_data.resample('QE').sum(numeric_only=True).reset_index()
monthly_sales_target_data = sales_target_data.resample('MS').sum(numeric_only=True).reset_index()
quarterly_sales_target_data = sales_target_data.resample('QE').sum(numeric_only=True).reset_index()

# Generate dummy customer list with recent visit details
customer_names = ['Customer A', 'Customer B', 'Customer C', 'Customer D', 'Customer E', 
                  'Customer F', 'Customer G', 'Customer H', 'Customer I', 'Customer J',
                  'Customer K', 'Customer L', 'Customer M', 'Customer N', 'Customer O']
visitor_names = ['Visitor X', 'Visitor Y', 'Visitor Z', 'Visitor W', 'Visitor V']
customer_list = pd.DataFrame({
    'Customer Name': np.random.choice(customer_names, 100),
    'Last Visit Date': pd.to_datetime(np.random.choice(pd.date_range('2024-01-01', '2024-12-31'), 100)),
    'Visitor Name': np.random.choice(visitor_names, 100)
})

# Streamlit app
st.set_page_config(
    page_title="Sales and Customer Visits Data Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('Sales and Customer Visits Data Viewer')

# 集計単位を選択するラジオボタン
aggregation_type = st.radio('Select Aggregation Type', ('Monthly', 'Quarterly'))

# 部署を選択するマルチセレクトボックス
departments = ['All Departments', 'Department A', 'Department B', 'Department C']
selected_departments = st.multiselect('Select Department(s)', departments, default='All Departments')

if aggregation_type == "Monthly":
    sales_data_to_display = monthly_sales_data
    sales_target_to_display = monthly_sales_target_data
else:
    sales_data_to_display = quarterly_sales_data
    sales_target_to_display = quarterly_sales_target_data

if "All Departments" in selected_departments:
    selected_departments = ['Department A', 'Department B', 'Department C']

filtered_customer_list = customer_list

# Combine actual sales and target sales data for Altair chart
combined_sales_data_actual = sales_data_to_display.melt(id_vars=['index'], var_name='Department', value_name='Sales')
combined_sales_data_target = sales_target_to_display.melt(id_vars=['index'], var_name='Department', value_name='Target')

combined_sales_data_actual['Type'] = 'Actual'
combined_sales_data_target['Type'] = 'Target'

combined_sales_data_actual = combined_sales_data_actual[combined_sales_data_actual['Department'].isin(selected_departments)]
combined_sales_data_target = combined_sales_data_target[combined_sales_data_target['Department'].isin(selected_departments)]

combined_sales_data_actual['Date'] = combined_sales_data_actual['index'].dt.strftime('%Y-%m')
combined_sales_data_target['Date'] = combined_sales_data_target['index'].dt.strftime('%Y-%m')

combined_sales_data_actual_long = pd.melt(combined_sales_data_actual, id_vars=['Date', 'Department'], value_vars=['Sales'])
combined_sales_data_target_long = pd.melt(combined_sales_data_target, id_vars=['Date', 'Department'], value_vars=['Target'])

combined_sales_data_long = pd.concat([combined_sales_data_actual_long, combined_sales_data_target_long])

# Display the grouped bar chart for actual sales and target sales using Altair
st.subheader(f'Sales Data by Department ({aggregation_type})')
sales_chart = alt.Chart(combined_sales_data_long).mark_bar().encode(
    column=alt.Column('Date:O', spacing=5, header=alt.Header(labelOrient="bottom", title=None)),
    x=alt.X('variable:N', sort=['Sales', 'Target'], axis=None),
    y=alt.Y('value:Q', title=None),
    color=alt.Color('variable:N', title=None)
).configure_view().properties(width=60, height=400)

st.altair_chart(sales_chart)

# Display the number of visits per customer as a horizontal bar chart using Altair
visit_counts = filtered_customer_list['Customer Name'].value_counts().reset_index()
visit_counts.columns = ['Customer Name', 'Visit Count']

st.subheader('Number of Visits per Customer')
visit_chart = alt.Chart(visit_counts).mark_bar().encode(
    x='Visit Count:Q',
    y=alt.Y('Customer Name:N', sort='-x')
).properties(
    width=600,
    height=400
)

st.altair_chart(visit_chart)

# Display the dummy customer list with recent visit details for the selected date range at the bottom of the page
st.subheader('Recent Customer Visits')
st.dataframe(filtered_customer_list)
