import os
import requests
import streamlit as st

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.title('Search Assistant')
query = st.text_input('Search query', placeholder='e.g. acoustic wall panel with FSC certification')
top_k = st.slider('Top K results', 1, 10, 5)
category = st.text_input('Optional category filter')
certification = st.text_input('Optional certification filter')

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Run semantic search', use_container_width=True):
        payload = {'query': query, 'top_k': top_k}
        response = requests.post(f'{API_BASE_URL}/search/semantic', json=payload)
        if response.ok:
            data = response.json()
            st.session_state['semantic_results'] = data['results']
        else:
            st.error(response.text)

with col2:
    if st.button('Run hybrid search', use_container_width=True):
        payload = {'query': query, 'top_k': top_k, 'category': category or None, 'certification': certification or None}
        response = requests.post(f'{API_BASE_URL}/search/hybrid', json=payload)
        if response.ok:
            data = response.json()
            st.session_state['hybrid_results'] = data['results']
        else:
            st.error(response.text)

with col3:
    if st.button('Ask grounded assistant', use_container_width=True):
        payload = {'query': query, 'top_k': top_k, 'category': category or None, 'certification': certification or None}
        response = requests.post(f'{API_BASE_URL}/chat/query', json=payload)
        if response.ok:
            st.session_state['chat_results'] = response.json()
        else:
            st.error(response.text)

if 'semantic_results' in st.session_state:
    st.subheader('Semantic search results')
    for item in st.session_state['semantic_results']:
        with st.container(border=True):
            st.write(f"**{item['product_name']}** — {item['supplier_name']}")
            st.write(f"Score: {item['score']}")
            st.caption(item['snippet'])

if 'hybrid_results' in st.session_state:
    st.subheader('Hybrid search results')
    for item in st.session_state['hybrid_results']:
        with st.container(border=True):
            st.write(f"**{item['product_name']}** — {item['supplier_name']}")
            st.write(f"Score: {item['score']} | Document ID: {item['document_id']}")
            st.caption(item['snippet'])

if 'chat_results' in st.session_state:
    st.subheader('Grounded assistant response')
    st.write(st.session_state['chat_results']['summary'])
    st.write(st.session_state['chat_results']['answer'])
    st.markdown('### Evidence')
    for item in st.session_state['chat_results']['evidence']:
        with st.container(border=True):
            st.write(f"Product ID: {item['product_id']} | Document ID: {item['document_id']} | Score: {item['score']}")
            st.caption(item['chunk_text'])
