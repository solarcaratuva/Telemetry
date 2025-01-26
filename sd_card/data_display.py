import streamlit as st

sd_data = open("./output/sample.txt", "r") # Using sample text file to demonstrate streamlit displaying file data 

st.title("SD Card")

st.subheader("The following is sample data from the sd card")

stuff = sd_data.read()

st.info(stuff)