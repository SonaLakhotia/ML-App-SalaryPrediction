import streamlit as st
from predict import show_predict_page
from explore import show_explore_page

page = st.sidebar.selectbox("Predict or Explore", ("Predict", "Explore"))

if page == "Explore":
    show_explore_page()
else:
    show_predict_page()