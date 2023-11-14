import pandas as pd
import streamlit as st
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
df_ipca_igpm = df_ipca_igpm[df_ipca_igpm['data'] >= '2023-01-01']

df_ipca_igpm['data'] = df_ipca_igpm['data'].dt.strftime('%Y-%m-%d')

#IIMPORTANDO OS DADOS DO IBOVESPA E DOLAR
ibov = yf.Ticker('^BVSP').history(period='12mo')
dolar = yf.Ticker('BRL=X').history(period='12mo')

df_ibov = pd.DataFrame()
df_dolar = pd.DataFrame()

df_ibov['Data'] = ibov['Close'].index
df_ibov['IBOV'] = list(ibov['Close'])

df_dolar['Data'] = dolar['Close'].index
df_dolar['Dólar'] = list(dolar['Close'])

#Pegando o valor do último fechamento para colocar no Painel
ibov_ult = ibov['Close'].iloc[-1:].values
dolar_ult = dolar['Close'].iloc[-1:].values
