import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import plost
import plotly.express as px
import plotly.graph_objects as go


#Consultando API
codigo_bcb = 4389

url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'

#Tratando os dados
df_cdi = pd.read_json(url)
df_cdi['data'] = pd.to_datetime(df_cdi['data'], dayfirst=True)

df_cdi = df_cdi[df_cdi['data'] >= '2002-08-01']
df_cdi = df_cdi.rename(columns={'valor':'CDI'}) 

# df_cdi.set_index('data', inplace=True)

#Configurando o Layout da Página
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

#Chamando o style.css da Página
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

col6, col7 = st.columns(2)

#Linha 2

with col6:
    tab1, tab2, tab3 = st.tabs(['CDI', 'IPCA','IGPM'])

    fig = px.line(df_cdi, x='data', y='CDI', title="CDI ao longo do Tempo")
    tab1.plotly_chart(fig)

with col7:
    tab1, tab2, tab3 = st.tabs(['Ibovespa', 'Dólar','WTI'])

    fig = px.line(df_cdi, x='data', y='CDI', title="CDI ao longo do Tempo")
    tab1.plotly_chart(fig)

#Rodapé do Sidebar
st.sidebar.markdown('''

**Mercedes Calculator** `version 2`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')