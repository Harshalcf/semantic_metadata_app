import os
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def load_secret(key):
    """Fetch secret from Streamlit Cloud or local .env"""
    return st.secrets.get(key)
