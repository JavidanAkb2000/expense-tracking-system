from datetime import datetime

import requests
import streamlit as st
import pandas as pd


API_URL = 'http://127.0.0.1:8000'

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input('End Date', datetime(2024, 8, 5))

    if st.button('Get Analytics'):
        payload = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }

        response = requests.post(f'{API_URL}/analytics/', json=payload)

        if response.status_code == 200:
           analytics_data = response.json()
           data = {
               'Category': list(analytics_data.keys()),
               'Total': [analytics_data[category]['total'] for category in analytics_data],
               'Percentage': [analytics_data[category]['percentage'] for category in analytics_data],
           }
           df = pd.DataFrame(data)
           st.dataframe(df)

           st.title('Expense Breakdown By Category')
           st.bar_chart(data=df.set_index('Category')['Percentage'])
        else:
            st.write('An error occured during HTTP request')