# app.py
# Streamlit UI — F1 Race Strategy Agent ke liye

import streamlit as st
from agent import run_agent

st.set_page_config(page_title="F1 Race Strategy Agent", page_icon="🏎️")

st.title("🏎️ F1 Race Strategy Agent")
st.write("Ask anything about an F1 driver, race, or season — the agent retrieves live data from OpenF1 and turns it into actionable insights through intelligent analysis.")

question = st.text_input("Ask anything:", placeholder="e.g. What tyre strategy did drivers use in the 2024 Monaco GP?")

if st.button("Ask") and question:
    with st.spinner("The agent is retrieving and analyzing live Formula 1 data..."):
        answer = run_agent(question)
    st.markdown(answer)

