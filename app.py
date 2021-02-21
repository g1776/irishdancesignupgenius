import streamlit as st
from selenium import webdriver
import selenium.webdriver.support.ui as ui

from main import *


st.title('Rochester Academy of Irish Dance')
st.text('SignUpGenius Automation')

email = st.text_input("Email", "")
password = st.text_input("Password", "")

go = st.button('Go!')

url_placeholder = st.empty()

if go:
    with st.spinner('Running...'):
        # progress bar
        latest_iteration = st.empty()
        bar = st.progress(0)
        sign_up_url = run(email, password, bar, st, latest_iteration)
        url_placeholder.text(f"Your Sign Up URL: {sign_up_url}")
