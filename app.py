# app.py
# Streamlit UI — F1 Race Strategy Agent ke liye

import streamlit as st
from agent import run_agent

st.set_page_config(page_title="F1 Race Strategy Agent", page_icon="🏎️")

st.title("🏎️ F1 Race Strategy Agent")
st.write("Kisi bhi driver, race, ya saal ke baare mein poocho — agent OpenF1 se live data nikaal ke analyze karega.")

question = st.text_input("Apna sawaal likho:", placeholder="e.g. What tyre strategy did drivers use in the 2024 Monaco GP?")

if st.button("Poocho") and question:
    with st.spinner("Agent data nikaal raha hai aur analyze kar raha hai..."):
        answer = run_agent(question)
    st.markdown(answer)
