import pandas as pd
import streamlit as st
import backend.liberar_produto_V2 as ro
import openpyxl as p
from streamlit_extras.app_logo import add_logo

def verificar_cnpj(cnpj):
    if cnpj=='' or cnpj==None:
        return False
    else:
        cnpj.strip().replace('-','').replace('.','').replace('/','')
        if not cnpj.isdigit():
            st.error(':red[ERRO: Esxiste algum item que não é numérico]', icon='🚨')
            return False
        elif len(cnpj)>14 or len(cnpj)<1:
            st.error(':red[ERRO: Quantidade de dígitos]', icon='🚨')
            return False
        return True


st.set_page_config(page_title='Liberar Produto')
# st.title('Desk Service Newe Seguros')
st.title(':green[Liberar Produto]')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
with st.container():    
    # recebendo os dados para montar o relatório
    st.write('---')
    server = st.selectbox(':violet[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
    cnpj = st.text_input(':violet[Digite o CNPJ: ]').strip()
    cdproduto = st.text_input(':violet[Digite o código I4PRO do produto: ]').strip()
    st.write('---')
with st.spinner('Wait for it...'):        
    if st.button('Atualizar valores'):   
        if verificar_cnpj(cnpj):
            st.write('---')
            df=ro.executar_processo(server, cnpj, cdproduto)
            st.write(':green[Banco atualizado]')
            st.write('---')
            df
            ro.config_log(server)
            







