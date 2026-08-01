import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0f1117;
        color: #e0e0e0;
    }

    section[data-testid="stSidebar"] {
        background-color: #161b27;
        border-right: 1px solid #1e2535;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #b0bac8 !important;
    }

    .sidebar-header {
        padding: 20px 16px 10px 16px;
        border-bottom: 1px solid #1e2535;
        margin-bottom: 0px;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff !important;
        margin: 0 0 4px 0;
        letter-spacing: -0.3px;
    }

    .sidebar-desc {
        font-size: 13px;
        color: #7a8799 !important;
        margin: 0;
        line-height: 1.5;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 6px;
        display: block;
        cursor: pointer;
        transition: background 0.2s;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: #1e2535;
    }

    section[data-testid="stSidebar"] .stRadio {
        margin-top: 0 !important;
    }

    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 22px;
        font-size: 14px;
        font-weight: 500;
        transition: background-color 0.2s;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
    }

    .stTextArea textarea, .stTextInput input {
        background-color: #1a2035;
        color: #e0e0e0;
        border: 1px solid #2a3550;
        border-radius: 6px;
        font-size: 14px;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #2563eb;
        outline: none;
        box-shadow: none;
    }

    .stFileUploader {
        background-color: #1a2035;
        border: 1.5px dashed #2a3550;
        border-radius: 8px;
        padding: 16px;
    }

    .stFileUploader label {
        color: #b0bac8 !important;
    }

    .stDataFrame, .stTable {
        background-color: #161b27;
        border-radius: 8px;
    }

    .stAlert {
        border-radius: 6px;
    }

    div[data-testid="stExpander"] {
        background-color: #161b27;
        border: 1px solid #1e2535;
        border-radius: 8px;
    }

    div[data-testid="stExpander"] summary {
        color: #e0e0e0;
        font-weight: 500;
    }

    .card {
        background-color: #161b27;
        border: 1px solid #1e2535;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }

    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .card-meta {
        font-size: 13px;
        color: #7a8799;
    }

    .answer-box {
        background-color: #161b27;
        border-left: 3px solid #2563eb;
        border-radius: 6px;
        padding: 18px 22px;
        color: #e0e0e0;
        font-size: 15px;
        line-height: 1.7;
        margin-top: 16px;
    }

    .source-tag {
        display: inline-block;
        background-color: #1e2a42;
        color: #6da3f8;
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 6px;
        font-weight: 500;
    }

    hr {
        border-color: #1e2535;
    }

    .stSpinner > div {
        border-top-color: #2563eb !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #1a2035;
        border-color: #2a3550;
    }

    .stMultiSelect div[data-baseweb="select"] {
        background-color: #1a2035;
        border-color: #2a3550;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #7a8799;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)
