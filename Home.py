import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import plost
import plotly.express as px
import plotly.graph_objects as go

#Acessando os Dados por API
codigo_bcb_cdi = 4389
codigo_bcb_ipca = 433
codigo_bcb_igpm = 189

url_cdi = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_cdi}/dados?formato=json'
url_ipca = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_ipca}/dados?formato=json'
url_igpm = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_igpm}/dados?formato=json'

#Convertendo Coluna de data em DateTime
df_cdi = pd.read_json(url_cdi)
df_cdi['data'] = pd.to_datetime(df_cdi['data'], dayfirst=True)

df_ipca = pd.read_json(url_ipca)
df_ipca['data'] = pd.to_datetime(df_ipca['data'], dayfirst=True)

df_igpm = pd.read_json(url_igpm)
df_igpm['data'] = pd.to_datetime(df_igpm['data'], dayfirst=True)

#Convertendo a frequência da data em Mensal
#Para isso é preciso indexar a DATA
df_igpm.set_index('data', inplace=True)
df_ipca.set_index('data', inplace=True)

df_igpm.index = df_igpm.index.to_period('M')
df_ipca.index = df_ipca.index.to_period('M')

#Renomeando as colunas pelos nomes dos Índices
df_ipca.rename(columns={'valor':'IPCA'}, inplace=True)
df_igpm.rename(columns={'valor':'IGPM'}, inplace=True)
df_cdi.rename(columns={'valor':'CDI'}, inplace=True) 

#Concatenando as Colunas pela Data
df_ipca_igpm = pd.concat([df_ipca,df_igpm], axis=1)

#Eliminando as linhas com NaN
df_ipca_igpm = df_ipca_igpm.dropna(axis=0)

#Resetando o Index
df_ipca_igpm.reset_index(inplace=True)

#Filtrando os dados a partir de uma data
df_cdi = df_cdi[df_cdi['data'] >= '2002-08-01']
df_ipca_igpm = df_ipca_igpm[df_ipca_igpm['data'] >= '2023-05-01']

df_ipca_igpm['data'] = df_ipca_igpm['data'].dt.strftime('%Y-%m-%d')

#Configurando o Layout da Página
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

#Chamando o style.css da Página
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Editando a primeira linha do Dashboardo com informações dos Índices
st.header('Benchmarks.')

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("CDI", "12,15%", "-0,50%")
col2.metric("IPCA (12m)", "4,82%", "0,24%")
col3.metric("IGPM (12m)", "-4,57%", "0,50%")
col4.metric("Ibovespa (Pts)", "120.568,14", "+1,29%")
col5.metric("Dólar", "R$4,91", "-0,51%")

col6, col7 = st.columns(2)

#Editando a segunda linha do Dashboard com Gráficos

with col6:
    tab1, tab2, tab3 = st.tabs(['CDI', 'IPCA','IGPM'])

    #Configurando o Gráfico do CDI
    fig_cdi = px.line(df_cdi, x='data', y='CDI', title="CDI ao longo do Tempo")

    #Configurando o Gráfico do IPCA e IGPM
    fig_ipca_igpm = px.bar(df_ipca_igpm, x='data', y='IPCA', title='IPCA')

    #Plotando o Gráfico na Tab
    tab1.plotly_chart(fig_cdi)
    tab2.plotly_chart(fig_ipca_igpm)

with col7:
    tab1, tab2, tab3 = st.tabs(['Ibovespa', 'Dólar','WTI'])

    #Configurando o Gráfico
    fig_cdi = px.line(df_cdi, x='data', y='CDI', title="CDI ao longo do Tempo")

    #Plotando o Gráfico na Tab
    tab1.plotly_chart(fig_cdi)

#Rodapé do Sidebar
st.sidebar.markdown('''

**Mercedes Calculator** `version 2`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')