import pandas as pd
import streamlit as st
import backend.Ajustar_Pagador_V2 as ro
import openpyxl as p
from homepage import diretorio_homepage
from streamlit_extras.app_logo import add_logo
import os
import subprocess
import streamlit.components.v1 as components
import keyboard
import time
import psutil
# from login import acesso
try:
    st.write('passei')
    with open('cred.txt','r') as arq:
        st.set_page_config(page_title='Ajustar Pagador')
        # st.title('Desk Service Newe Seguros')
        st.title(':green[Ajustar Pagador]')
        add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)

        with st.container():

            # recebendo os dados para montar o relatório
            server = st.selectbox(':green[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
            cd_apolice = st.text_input(':green[Digite o nome codigo da apólice / proposta]')
            nr_endosso = st.text_input(':green[Digite o número do endosso:] ')
            nr_parcela = st.text_input(":green[Digite o número da parcela: ] ")
            tipo_subvencao = st.selectbox(':green[Digite o tipo subvenção: ]',options=('Subvenção Federal', 'Subvenção Estadual e Federal', 'Segurado' ))
            if tipo_subvencao == 'Subvenção Federal':
                cod = 1
            elif tipo_subvencao == 'Subvenção Estadual e Federal':
                cod = 2
            elif tipo_subvencao == 'Segurado':
                cod='NULL'

        with st.spinner('Wait for it...'):        
            if st.button('Atualizar valores'):   
                df=ro.executar_processo(server,cd_apolice,nr_endosso,nr_parcela,cod)
                st.success('Banco atualizado')
                df
                ro.config_log(server)

except:
        st.error('pegaaaa')
        diretorio_atual = os.path.abspath(os.getcwd())
        # path_home='http://localhost:8508/'
        
        
        # components.iframe(path_home)
        if diretorio_atual == diretorio_homepage:
            
            subprocess.run(["streamlit", "run", "homepage.py"])
        else:
            diretorio_pai = os.path.dirname(diretorio_atual)
            os.chdir(diretorio_pai)             
            subprocess.run(["streamlit", "run", "homepage.py"])





