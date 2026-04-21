import os
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.title('Product Directory')

products = requests.get(f'{API_BASE_URL}/products').json()
if not products:
    st.info('No products yet. Upload and process a supplier document first.')
    st.stop()

rows = []
for p in products:
    rows.append({
        'ID': p['id'],
        'Name': p['product_name'],
        'Category': p.get('category'),
        'Brand': p.get('brand'),
        'Confidence': p.get('confidence_score'),
        'Attributes': ', '.join(f"{a['attribute_name']}: {a.get('attribute_value','')} {a.get('unit','') or ''}" for a in p.get('attributes', []))
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)

product_ids = [p['id'] for p in products]
selected = st.selectbox('Inspect a product', product_ids)
product = requests.get(f'{API_BASE_URL}/products/{selected}').json()

st.subheader(product['product_name'])
st.write(f"Category: {product.get('category')} | Brand: {product.get('brand')} | Confidence: {product.get('confidence_score')}")
st.write(product.get('description'))

st.markdown('### Extracted attributes')
for attr in product.get('attributes', []):
    with st.container(border=True):
        st.write(f"**{attr['attribute_name']}**: {attr.get('attribute_value')} {attr.get('unit') or ''}")
        if attr.get('source_snippet'):
            st.caption(attr['source_snippet'])
