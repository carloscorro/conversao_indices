import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import plost
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import numpy as np

#ACESSANDO OS DADOS POR API DO CDI, IPCA E IGPM
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
df_ipca_igpm = df_ipca_igpm[df_ipca_igpm['data'] >= '2023-01-01']

df_ipca_igpm['data'] = df_ipca_igpm['data'].dt.strftime('%Y-%m-%d')

######################======================#######################

#IIMPORTANDO OS DADOS DO IBOVESPA E DOLAR
ibov = yf.Ticker('^BVSP').history(period='12mo')
dolar = yf.Ticker('BRL=X').history(period='12mo')
crude = yf.Ticker('CL=F').history(period='12mo')

df_ibov = pd.DataFrame()
df_dolar = pd.DataFrame()
df_crude = pd.DataFrame()

df_ibov['Data'] = ibov['Close'].index
df_ibov['IBOV'] = list(ibov['Close'])
df_ibov['Data'] = df_ibov['Data'].dt.strftime('%Y-%m-%d')

df_dolar['Data'] = dolar['Close'].index
df_dolar['Dolar'] = list(dolar['Close'])
df_dolar['Data'] = df_dolar['Data'].dt.strftime('%Y-%m-%d')

df_crude['Data'] = crude['Close'].index
df_crude['Crude'] = list(crude['Close'])
df_crude['Data'] = df_crude['Data'].dt.strftime('%Y-%m-%d')

#Pegando o valor do último fechamento para colocar no Painel
ibov_ult = round(df_ibov['IBOV'].iloc[-1],2)
atual_ibov = '{0:,}'.format(ibov_ult).replace(',','.')
ibov_ult_2 = round(df_ibov['IBOV'].iloc[-2],2)
delta_ibov = round(((ibov_ult / ibov_ult_2) - 1) * 100,2)

dol_ult = round(df_dolar['Dolar'].iloc[-1],2)
atual_dol = '{0:,}'.format(dol_ult).replace('.',',')
dol_ult_2 = round(df_dolar['Dolar'].iloc[-2],2)
delta_dol = round(((dol_ult / dol_ult_2) - 1) * 100,2)

crude_ult = round(df_crude['Crude'].iloc[-1],2)
atual_crude = '{0:,}'.format(crude_ult).replace('.',',')
crude_ult_2 = round(df_crude['Crude'].iloc[-2],2)
delta_crude = round(((crude_ult / crude_ult_2) - 1) * 100,2)

######################======================#######################

#Configurando o Layout da Página
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

#Chamando o style.css da Página
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Editando a primeira linha do Dashboardo com informações dos Índices
st.header('Benchmarks.')

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("CDI", "12,15%", "-0,50%")
col2.metric("IPCA (12m)", "4,82%", "0,24%")
col3.metric("IGPM (12m)", "-4,57%", "0,50%")
col4.metric(label='Ibovespa(pts)', value=atual_ibov, delta=delta_ibov)
col5.metric(label='Dólar', value=atual_dol, delta=delta_dol)
col6.metric(label='Crude Oil', value=atual_crude, delta=delta_crude)

col6, col7 = st.columns(2)

#Editando a segunda linha do Dashboard com Gráficos

with col6:
    tab1, tab2, tab3 = st.tabs(['CDI', 'IPCA','IGPM'])

    #Configurando o Gráfico do CDI
    fig_cdi = px.line(df_cdi, x='data', y='CDI', title="CDI")

    #Configurando o Gráfico do IPCA
    fig_ipca = px.bar(df_ipca_igpm, x='data', y='IPCA', title='IPCA(%) ao mês')

    #Configurando o Gráfico do IGPM
    fig_igpm = px.bar(df_ipca_igpm, x='data', y='IGPM', title='IGPM(%) ao mês')

    #Plotando o Gráfico na Tab
    tab1.plotly_chart(fig_cdi)
    tab2.plotly_chart(fig_ipca)
    tab3.plotly_chart(fig_igpm)
    

with col7:
    tab1, tab2, tab3 = st.tabs(['Ibovespa', 'Dólar','Crude Oil'])

    #Configurando o Gráfico
    fig_ibov = px.line(df_ibov, x='Data', y='IBOV', title="Ibovespa")
    fig_dol = px.line(df_dolar, x='Data', y='Dolar', title="Dólar")
    fig_crude = px.line(df_crude, x='Data', y='Crude', title="Crude Oil")

    #Plotando o Gráfico na Tab
    tab1.plotly_chart(fig_ibov)
    tab2.plotly_chart(fig_dol)
    tab3.plotly_chart(fig_crude)

#Rodapé do Sidebar
st.sidebar.markdown('''

**Mercedes Calculator** `version 1.1`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')