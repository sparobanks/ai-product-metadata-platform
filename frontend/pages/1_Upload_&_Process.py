import os
import requests
import streamlit as st

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.title('Upload & Process Documents')

supplier_name = st.text_input('Supplier name', value='EcoBuild Materials')
document_type = st.selectbox('Document type', ['spec_sheet', 'brochure', 'compliance_doc', 'sustainability_doc'])
uploaded_file = st.file_uploader('Upload a product PDF or image', type=['pdf', 'png', 'jpg', 'jpeg'])

if st.button('Upload document', use_container_width=True):
    if not uploaded_file:
        st.warning('Please choose a file first.')
    else:
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {'supplier_name': supplier_name, 'document_type': document_type}
        response = requests.post(f'{API_BASE_URL}/documents/upload', files=files, data=data)
        if response.ok:
            st.success('Document uploaded successfully')
            st.json(response.json())
        else:
            st.error(response.text)

st.markdown('---')
st.subheader('Uploaded documents')
try:
    docs = requests.get(f'{API_BASE_URL}/documents').json()
except Exception as exc:
    st.error(exc)
    docs = []

for doc in docs:
    with st.container(border=True):
        st.write(f"**#{doc['id']}** — {doc['filename']} ({doc['document_type']})")
        st.write(f"Supplier ID: {doc['supplier_id']} | Status: {doc['parse_status']} | OCR used: {doc['ocr_used']}")
        cols = st.columns([1, 1, 3])
        with cols[0]:
            if st.button(f"Process #{doc['id']}", key=f"process_{doc['id']}"):
                resp = requests.post(f"{API_BASE_URL}/documents/{doc['id']}/process")
                if resp.ok:
                    st.success(f"Processed document #{doc['id']}")
                    st.json(resp.json())
                else:
                    st.error(resp.text)
        with cols[1]:
            if doc.get('extracted_text'):
                st.download_button(
                    f"Download text #{doc['id']}",
                    doc['extracted_text'],
                    file_name=f"document_{doc['id']}_text.txt",
                    key=f"download_{doc['id']}"
                )
        with cols[2]:
            if doc.get('extracted_text'):
                st.text_area('Extracted text preview', value=doc['extracted_text'][:1200], height=180, key=f"txt_{doc['id']}")
