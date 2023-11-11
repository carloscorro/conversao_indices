import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

codigo_bcb = 4389

url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'

df_cdi = pd.read_json(url)
df_cdi['data'] = pd.to_datetime(df_cdi['data'], dayfirst=True)

df_cdi = df_cdi[df_cdi['data'] >= '2001-01-01']

df_cdi = df_cdi.rename(columns={'valor':'CDI'}) 

df_cdi.set_index('data', inplace=True)

print(df_cdi)