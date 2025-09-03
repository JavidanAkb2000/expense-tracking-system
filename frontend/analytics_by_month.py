from datetime import datetime

import requests
import streamlit as st
import pandas as pd

API_URL = 'http://127.0.0.1:8000'


def analytics_month():
    st.subheader('Monthly Expense')

    # Initialize empty dataframe
    data = pd.DataFrame({
        'Month_Name': [],
        'Total': []
    })

    if st.button('Get Monthly Analytics'):
        response = requests.get(f'{API_URL}/analytics_by_month/')
        if response.status_code == 200:
            monthly_data = response.json()

            # Create lists to store data
            month_names = []
            totals = []

            for month in monthly_data:
                month_names.append(month['month_name'])
                totals.append(month['total'])

            # Create dataframe with the data
            data = pd.DataFrame({
                'Month_Name': month_names,
                'Total': totals
            })
        else:
            st.error("Failed to fetch monthly analytics")

    # Display table and chart
    st.dataframe(data)

    if not data.empty:
        st.bar_chart(data.set_index('Month_Name')['Total'])
    else:
        st.info("Click 'Get Monthly Analytics' to view data")