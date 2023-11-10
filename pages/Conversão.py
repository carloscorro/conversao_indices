import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image

#Título 
st.header('Conversão de índices.')

indice_input = st.radio(
    "Selecione o índice:",
    ("CDI", "IPCA", "IGPM")
)

taxa_pre_input = st.number_input(
    "Digite a taxa pré-fixada do título:"
)

#taxas 
cdi_indice = 0.1215
ipca_indice = 0.0463
igpm_indice = 0.0446
taxa_pre_input = taxa_pre_input / 100


if indice_input == "CDI":
    taxa_nominal_input = (1+cdi_indice)*(1+taxa_pre_input)-1
elif indice_input == "IPCA":
    taxa_nominal_input = (1+ipca_indice)*(1+taxa_pre_input)-1
elif indice_input == "IGPM":
    taxa_nominal_input = (1+igpm_indice)*(1+taxa_pre_input)-1

indice_converte = st.radio(
    "Selecione o índice que deseja converter:",
    ("CDI", "IPCA", "IGPM")
)

if indice_converte == "CDI":
    taxa_pre_convert = (1 + taxa_nominal_input) / (1 + cdi_indice) - 1  
elif indice_converte == "IPCA":
    taxa_pre_convert = (1 + taxa_nominal_input) / (1 + ipca_indice) - 1
elif indice_converte == "IGPM":
    taxa_pre_convert = (1 + taxa_nominal_input) / (1 + igpm_indice) - 1

taxa_pre_convert = round(taxa_pre_convert * 100,2)

if st.button("Converter!") == True:
    st.subheader(f"{indice_converte} + {taxa_pre_convert}%")
