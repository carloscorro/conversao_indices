import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.header('Benchmarks')

col1, col2, col3, col4 = st.columns(4)
col1.metric("CDI", "12,15%", "-0,50%")
col2.metric("IPCA (12m)", "4,82%", "0,24%")
col3.metric("IGPM (12m)", "-4,57%", "0,50%")
col4.metric("Dólar", "R$4,91", "-0,51%")