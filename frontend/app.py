from datetime import datetime

import requests
import streamlit as st
import pandas as pd

# st.title("Expense Tracking System")
#
# expense_dt = st.date_input('Expense Date: ')
# name = st.text_input('Enter your name', placeholder='Enter your name')
#
# if expense_dt:
#     st.write(f"Fetching expenses for {expense_dt}")
#
# if name:
#     st.write(f"Fetching expenses for {name}")


# # Text elements
# st.header('Streamlit Core Features')
# st.subheader('Text Elements')
# st.text('This is a simple text element')
#
# # Data Display
# st.subheader('Data Display')
# st.write('Here is a simple table: ')
# st.table(
#     {
#         'Column 1': [1, 2, 3],
#         'Column 2': [4, 5, 6],
#     }
# )
#
# # Charts
# st.subheader('Charts')
# st.line_chart([0, 1, 2, 3, 4])
#
# # DataFrame
# df = pd.DataFrame({
#     'Date': ['2024-08-01', '2024-08-02', '2024-08-03'],
#     'Amount': [250, 134, 340]
# })
#
# st.subheader('More interactive dataframe')
# st.dataframe(df) # more interactive
#
# st.subheader('Simple dataframe')
# st.table(df)


# st.title('Interactive Widget Example')
#
# # Checkbox
# if st.checkbox('Show/Hide'):
#     st.write('Checkbox is checked')


# # Multiselect
# option = st.multiselect('Select multiple number', [1, 2, 3, 4])
# st.write(f'You selected: {option}')
#
# # Selectbox
#
# options = st.selectbox('Category', ['Rent', 'Food'], label_visibility='collapsed')
# st.write(f'You selected: {options}')
#
#
#
#




from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from analytics_by_month import analytics_month
st.title('Expense Tracking System')

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics', 'Analytics By Months'])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_month()
