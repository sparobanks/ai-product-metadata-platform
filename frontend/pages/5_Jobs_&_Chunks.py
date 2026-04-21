import os
import requests
import streamlit as st

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.title('Jobs & Chunks')

jobs = requests.get(f'{API_BASE_URL}/jobs').json()
st.subheader('Processing jobs')
if not jobs:
    st.info('No jobs yet.')
else:
    for job in jobs:
        with st.container(border=True):
            st.write(f"**Job #{job['id']}** — Document {job['document_id']}")
            st.write(f"Status: {job['status']} | Stage: {job['stage']}")
            st.caption(job['message'])

st.markdown('---')
document_id = st.number_input('Load chunks for document ID', min_value=1, step=1)
if st.button('Load chunks', use_container_width=True):
    response = requests.get(f'{API_BASE_URL}/chunks/document/{document_id}')
    if response.ok:
        chunks = response.json()
        if not chunks:
            st.info('No chunks found for that document.')
        for chunk in chunks:
            with st.container(border=True):
                st.write(f"Chunk #{chunk['chunk_index']} | Product ID: {chunk['product_id']}")
                st.caption(chunk['chunk_text'])
    else:
        st.error(response.text)
