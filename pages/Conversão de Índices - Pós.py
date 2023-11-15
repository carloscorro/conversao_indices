import streamlit as st
import pandas as pd 
import time

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cabeçalho 
st.header('Conversão de Índice - Pós.')


taxa_pre_input = st.number_input(
    "Digite a porcentagem do CDI para conversão (Ex: 100%):"
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

taxa_cdi_nominal = taxa_pre_input * cdi_indice

if st.button("Converter!") == True:
    with st.spinner('Calculando...'):
        time.sleep(1)
        st.subheader(f"Taxa nominal ao ano: {round(taxa_cdi_nominal * 100,2)}%")
        if indice_converte == "CDI":
            taxa_pre_convert = (1 + taxa_cdi_nominal) / (1 + cdi_indice) - 1
            if taxa_pre_convert < 0:
                st.subheader(f"{indice_converte} - {round(taxa_pre_convert * 100 *-1,2)}%")
            else:
                st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")
        elif indice_converte == "IPCA":
            taxa_pre_convert = (1 + taxa_cdi_nominal) / (1 + ipca_indice) - 1
            if taxa_pre_convert < 0:
                st.subheader(f"{indice_converte} - {round(taxa_pre_convert * 100 *-1,2)}%")
            else:
                st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")
        elif indice_converte == "IGPM":
            taxa_pre_convert = (1 + taxa_cdi_nominal) / (1 + igpm_indice) - 1
            if taxa_pre_convert < 0:
                st.subheader(f"{indice_converte} - {round(taxa_pre_convert * 100 *-1,2)}%")
            else:
                st.subheader(f"{indice_converte} + {round(taxa_pre_convert * 100,2)}%")

st.sidebar.markdown('''

Mercedes Calculator `version 1.1`
                    
Created by [Carlos Mercedes](https://www.linkedin.com/in/carlos-mercedes-121096165/).
''')