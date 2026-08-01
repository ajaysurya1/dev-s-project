import streamlit as st

st.set_page_config(
    page_title="DocMind",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

from views import upload_page, documents_page, ask_page
from styles import apply_styles

apply_styles()

PAGES = {
    "Upload": upload_page.show,
    "Documents": documents_page.show,
    "Ask": ask_page.show,
}

st.sidebar.markdown(
    "<div class='sidebar-header'>"
    "<p class='sidebar-title'>DocMind</p>"
    "<p class='sidebar-desc'>Ask questions across your uploaded documents.</p>"
    "</div>",
    unsafe_allow_html=True
)

selected_page = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

PAGES[selected_page]()
