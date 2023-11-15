import streamlit as st
import pandas as pd
import yfinance as yf
import plotly
import plotly.express as px
import time

#ACESSANDO OS DADOS POR API DO CDI, IPCA E IGPM
codigos_bcb = [4389, 433, 189]
indices_bcb = ['CDI', 'IPCA', 'IGPM']

df_cdi = pd.DataFrame()
df_ipca = pd.DataFrame()
df_igpm = pd.DataFrame()

def tratar_dados(cod):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json'
    df = pd.read_json(url)
    #Convertendo Coluna de data em DateTime
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    return df

for cod, i in zip(codigos_bcb, indices_bcb):
    if i == 'CDI':
        df_cdi = tratar_dados(cod)            
    if i == 'IPCA':
        df_ipca = tratar_dados(cod)            
    if i == 'IGPM':
        df_igpm = tratar_dados(cod)            

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
tickers = ['^BVSP', 'BRL=X', 'CL=F']
indices = ['IBOV', 'Dolar', 'Crude']

def tratar_df(ticker, indice):
    ticker = yf.Ticker(ticker).history(period='12mo')
    df = pd.DataFrame()
    df['Data'] = ticker['Close'].index
    df[indice] = list(ticker['Close'])
    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
    return df

df_ibov = pd.DataFrame()
df_dol = pd.DataFrame()
df_crude = pd.DataFrame()

for t, i in zip(tickers, indices):
    if t == '^BVSP':
        df_ibov = tratar_df(t, i)
        ibov_ult = round(df_ibov[i].iloc[-1],2)
        ibov_ult_2 = round(df_ibov[i].iloc[-2],2)
        delta_ibov = round(((ibov_ult / ibov_ult_2) - 1) * 100,2)
        atual_ibov = '{0:,}'.format(ibov_ult).replace(',','.')
    elif t == 'BRL=X': 
        df_dol = tratar_df(t,i)
        dol_ult = round(df_dol[i].iloc[-1],2)
        atual_dol = '{0:,}'.format(dol_ult).replace('.',',')
        dol_ult_2 = round(df_dol[i].iloc[-2],2)
        delta_dol = round(((dol_ult / dol_ult_2) - 1) * 100,2)
    elif t == 'CL=F':
        df_crude = tratar_df(t,i)   
        crude_ult = round(df_crude[i].iloc[-1],2)
        atual_crude = '{0:,}'.format(crude_ult).replace('.',',')
        crude_ult_2 = round(df_crude[i].iloc[-2],2)
        delta_crude = round(((crude_ult / crude_ult_2) - 1) * 100,2)

######################======================########################

#Configurando o Layout da Página
st.set_page_config(layout="wide", initial_sidebar_state="expanded",)

#Chamando o style.css da Página
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Editando a primeira linha do Dashboardo com informações dos Índices
st.header('Benchmarks.')

wid_col = 5

col1, col2, col3, col4, col5, col6 = st.columns([wid_col,wid_col,wid_col,wid_col,wid_col,wid_col])
col1.metric("CDI", "12,15%", "-0,50%")
col2.metric("IPCA (12m)", "4,82%", "0,24%")
col3.metric("IGPM (12m)", "-4,57%", "0,50%")
col4.metric(label='Ibovespa(pts)', value=atual_ibov, delta=delta_ibov)
col5.metric(label='Dólar', value=atual_dol, delta=delta_dol)
col6.metric(label='Crude Oil', value=atual_crude, delta=delta_crude)

col7, col8 = st.columns(2)

#Editando a segunda linha do Dashboard com Gráficos

with col7:
    tab1, tab2, tab3 = st.tabs(['CDI', 'IPCA','IGPM'])

    #Configurando o Gráfico do CDI
    fig_cdi = px.line(df_cdi, x='data', y='CDI', title="CDI", width=580)

    #Configurando o Gráfico do IPCA
    fig_ipca = px.bar(df_ipca_igpm, x='data', y='IPCA', title='IPCA(%) ao mês', width=580)

    #Configurando o Gráfico do IGPM
    fig_igpm = px.bar(df_ipca_igpm, x='data', y='IGPM', title='IGPM(%) ao mês',width=580)

    #Plotando o Gráfico na Tab
    tab1.plotly_chart(fig_cdi)
    tab2.plotly_chart(fig_ipca)
    tab3.plotly_chart(fig_igpm)
    

with col8:
    tab3, tab4, tab5 = st.tabs(['Ibovespa', 'Dólar','Crude Oil'])

    #Configurando o Gráfico
    fig_ibov = px.line(df_ibov, x='Data', y='IBOV', title="Ibovespa", width=580)
    fig_dol = px.line(df_dol, x='Data', y='Dolar', title="Dólar", width=580)
    fig_crude = px.line(df_crude, x='Data', y='Crude', title="Crude Oil", width=580)

    #Plotando o Gráfico na Tab
    tab3.plotly_chart(fig_ibov)
    tab4.plotly_chart(fig_dol)
    tab5.plotly_chart(fig_crude)

#Rodapé do Sidebar
st.sidebar.markdown('''

**Mercedes Calculator** `version 1.1`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')