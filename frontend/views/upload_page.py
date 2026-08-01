import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import upload_file, check_health, BASE_URL


def show():
    st.markdown("## Upload Document")
    st.markdown("Upload a file to extract its text and make it available for questions.")
    st.markdown("---")

    backend_ok = check_health()
    if not backend_ok:
        st.error("Backend is not reachable.  " + BASE_URL)
        return

    allowed_types = ["pdf", "docx", "txt", "csv", "png", "jpg", "jpeg"]

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=allowed_types,
        help="Supported formats: PDF, DOCX, TXT, CSV, PNG, JPG, JPEG"
    )

    if uploaded_file is not None:
        file_size_kb = round(uploaded_file.size / 1024, 1)

        col1, col2, col3 = st.columns(3)
        col1.metric("File Name", uploaded_file.name)
        col2.metric("File Size", str(file_size_kb) + " KB")
        col3.metric("File Type", uploaded_file.type.split("/")[-1].upper())

        st.markdown("")

        if st.button("Upload and Process"):
            with st.spinner("Uploading and extracting text..."):
                response = upload_file(uploaded_file.getvalue(), uploaded_file.name)

            if response.status_code == 200:
                data = response.json()
                st.success(
                    "File uploaded successfully. "
                    + str(data["chunk_count"]) + " chunks were created from this document."
                )
                st.markdown(
                    "<div class='card'>"
                    "<div class='card-title'>" + data["name"] + "</div>"
                    "<div class='card-meta'>Document ID: " + str(data["document_id"]) + "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                error_message = "Upload failed."
                try:
                    error_message = response.json().get("detail", error_message)
                except Exception:
                    pass
                st.error(error_message)
