import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import plost

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Linha 1
st.header('Benchmarks.')

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("CDI", "12,15%", "-0,50%")
col2.metric("IPCA (12m)", "4,82%", "0,24%")
col3.metric("IGPM (12m)", "-4,57%", "0,50%")
col4.metric("Ibovespa (Pts)", "120.568,14", "+1,29%")
col5.metric("Dólar", "R$4,91", "-0,51%")


st.sidebar.markdown('''

**Mercedes Calculator** `version 2`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')