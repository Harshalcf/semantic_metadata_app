# import os
# import streamlit as st

# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except:
#     pass

# def load_secret(key):
#     """Fetch secret from Streamlit Cloud or local .env"""
#     return os.getenv(key)


import os
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def load_secret(key):
    try:
        # Ye try block handle karega jab streamlit ke secrets available nahi hote local mein
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    # Local ke liye fallback
    env_var = os.getenv(key)
    if env_var:
        return env_var

    # Error display karo aur process fail karao
    raise ValueError(f"Key '{key}' not found in secrets or .env")


