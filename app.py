import streamlit as st
from main import run

st.sidebar.text_input("Chrome Version", "89.0.4389")


st.title('Rochester Academy of Irish Dance')
st.text('SignUpGenius Automation')

try:
    import credentials
    email = st.text_input("Email", credentials.EMAIL)
    password = st.text_input("Password", credentials.PASSWORD)
except:
    email = st.text_input("Email", "")
    password = st.text_input("Password", "")

go = st.button('Go!')

url_placeholder = st.empty()

if go:
    with st.spinner('Running...'):
        # progress bar
        latest_iteration = st.empty()
        bar = st.progress(0)
        sign_up_url = run(email, password, bar, st, latest_iteration, chrome_version)
        url_placeholder.text(f"Your Sign Up URL: {sign_up_url}")
