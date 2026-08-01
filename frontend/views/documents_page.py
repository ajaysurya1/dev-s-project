import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import get_documents, delete_document, preview_document


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return str(size_bytes) + " B"
    size_kb = size_bytes / 1024
    if size_kb < 1024:
        return str(round(size_kb, 1)) + " KB"
    size_mb = size_kb / 1024
    return str(round(size_mb, 2)) + " MB"


def show():
    st.markdown("## Documents")
    st.markdown("All uploaded documents are listed here. You can preview or delete them.")
    st.markdown("---")

    response = get_documents()

    if response.status_code != 200:
        st.error("Could not load documents. Is the backend running?")
        return

    documents = response.json()

    if len(documents) == 0:
        st.info("No documents uploaded yet. Go to the Upload page to add one.")
        return

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Documents", len(documents))
    total_chunks = sum(doc["chunk_count"] for doc in documents)
    col_b.metric("Total Chunks", total_chunks)
    total_size = sum(doc["file_size"] for doc in documents)
    col_c.metric("Total Size", format_file_size(total_size))

    st.markdown("")

    for document in documents:
        with st.expander(document["name"]):
            detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
            detail_col1.markdown("**Type:** " + document["file_type"].upper())
            detail_col2.markdown("**Size:** " + format_file_size(document["file_size"]))
            detail_col3.markdown("**Chunks:** " + str(document["chunk_count"]))
            detail_col4.markdown("**Uploaded:** " + document["upload_time"][:10])

            st.markdown("")

            button_col1, button_col2, _ = st.columns([1, 1, 5])

            with button_col1:
                if st.button("Preview", key="preview_" + str(document["id"])):
                    preview_response = preview_document(document["id"])
                    if preview_response.status_code == 200:
                        preview_data = preview_response.json()
                        st.markdown("**Characters extracted:** " + str(preview_data["character_count"]))
                        st.text_area(
                            "Extracted text preview",
                            value=preview_data["extracted_text"][:2000],
                            height=220,
                            disabled=True,
                            key="text_preview_" + str(document["id"])
                        )
                    else:
                        st.error("Could not load preview.")

            with button_col2:
                if st.button("Delete", key="delete_" + str(document["id"])):
                    delete_response = delete_document(document["id"])
                    if delete_response.status_code == 200:
                        st.success("Document deleted.")
                        st.rerun()
                    else:
                        st.error("Could not delete document.")
