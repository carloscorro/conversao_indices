import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Cabeçalho
st.header('Taxa Equivalente.')

taxa_opcao = st.selectbox(
    "Selecione o tipo de taxa (Ano ou Mês):",
    ("Taxa ao mês (a.m.)", "Taxa ao ano (a.a.)")
)

taxa_pre_input = st.number_input(
    "Digite a taxa pré-fixada:"
)

indice_converte = st.radio(
    "Selecione o índice que deseja converter:",
    ("CDI", "IPCA", "IGPM")
)

#taxas 
cdi_indice = 0.1215
ipca_indice = 0.0463
igpm_indice = 0.0446
taxa_pre_input = taxa_pre_input / 100


if st.button("Converter!") == True:
    if taxa_opcao == "Taxa ao mês (a.m.)":
        juros_ao_ano = round((((1 + taxa_pre_input) ** 12) - 1)*100,2)
        juros_ao_ano_nominal = (((1 + taxa_pre_input) ** 12) - 1)
        st.subheader(f"Juros ao ano: {juros_ao_ano}%")
        if indice_converte == "CDI":
            taxa_pre_convert = (1 + juros_ao_ano_nominal) / (1 + cdi_indice) - 1
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")  
        elif indice_converte == "IPCA":
            taxa_pre_convert = (1 + juros_ao_ano_nominal) / (1 + ipca_indice) - 1
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")
        elif indice_converte == "IGPM":
            taxa_pre_convert = (1 + juros_ao_ano_nominal) / (1 + igpm_indice) - 1
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")
    else :
        juros_ao_mes = round((((1 + taxa_pre_input) ** (1/12)) - 1)*100,2)
        if indice_converte == "CDI":
            taxa_pre_convert = (1 + taxa_pre_input) / (1 + cdi_indice) - 1
            st.subheader(f"Juros ao mês: {juros_ao_mes}%")
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")  
        elif indice_converte == "IPCA":
            st.subheader(f"Juros ao mês: {juros_ao_mes}%")
            taxa_pre_convert = (1 + taxa_pre_input) / (1 + ipca_indice) - 1
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")
        elif indice_converte == "IGPM":
            taxa_pre_convert = (1 + taxa_pre_input) / (1 + igpm_indice) - 1
            st.subheader(f"Juros ao mês: {juros_ao_mes}%")
            st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")

st.sidebar.markdown('''

Mercedes Calculator `version 2`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')