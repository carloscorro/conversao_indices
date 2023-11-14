import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import MetaTrader5 as mt5
from datetime import datetime
import time 
import requests
import yfinance as yf
import numpy as np

# #Acessando os Dados por API
# codigo_bcb_cdi = 4389
# codigo_bcb_ipca = 433
# codigo_bcb_igpm = 189

# url_cdi = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_cdi}/dados?formato=json'
# url_ipca = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_ipca}/dados?formato=json'
# url_igpm = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb_igpm}/dados?formato=json'

# #Convertendo Coluna de data em DateTime
# df_cdi = pd.read_json(url_cdi)
# df_cdi['data'] = pd.to_datetime(df_cdi['data'], dayfirst=True)

# df_ipca = pd.read_json(url_ipca)
# df_ipca['data'] = pd.to_datetime(df_ipca['data'], dayfirst=True)

# df_igpm = pd.read_json(url_igpm)
# df_igpm['data'] = pd.to_datetime(df_igpm['data'], dayfirst=True)

# #Convertendo a frequência da data em Mensal
# #Para isso é preciso indexar a DATA
# df_igpm.set_index('data', inplace=True)
# df_ipca.set_index('data', inplace=True)

# df_igpm.index = df_igpm.index.to_period('M')
# df_ipca.index = df_ipca.index.to_period('M')

# #Renomeando as colunas pelos nomes dos Índices
# df_ipca.rename(columns={'valor':'IPCA'}, inplace=True)
# df_igpm.rename(columns={'valor':'IGPM'}, inplace=True)
# df_cdi.rename(columns={'valor':'CDI'}, inplace=True) 

# #Concatenando as Colunas pela Data
# df_ipca_igpm = pd.concat([df_ipca,df_igpm], axis=1)

# #Eliminando as linhas com NaN
# df_ipca_igpm = df_ipca_igpm.dropna(axis=0)

# #Resetando o Index
# df_ipca_igpm.reset_index(inplace=True)

# #Filtrando os dados a partir de uma data
# df_cdi = df_cdi[df_cdi['data'] >= '2002-08-01']
# df_ipca_igpm = df_ipca_igpm[df_ipca_igpm['data'] >= '2023-01-01']

# df_ipca_igpm['data'] = df_ipca_igpm['data'].dt.strftime('%Y-%m-%d')

##########################################33

#Importando os dados do Ibovespa e Dólar
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

print(df_crude)