import os
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.title('Validation Dashboard')

products = requests.get(f'{API_BASE_URL}/products').json()
if products:
    selected = st.selectbox('Re-run validation for product', [p['id'] for p in products])
    if st.button('Run validation', use_container_width=True):
        response = requests.post(f'{API_BASE_URL}/validation/run/{selected}')
        if response.ok:
            st.success(response.json()['message'])
        else:
            st.error(response.text)

issues = requests.get(f'{API_BASE_URL}/validation/issues').json()
if not issues:
    st.info('No validation issues yet.')
else:
    st.dataframe(pd.DataFrame(issues), use_container_width=True)
