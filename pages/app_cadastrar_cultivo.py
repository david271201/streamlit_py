import pandas as pd
import streamlit as st
import backend.cadastrar_cultivo_V2 as ro
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
    
st.set_page_config(page_title='Cadastrar Cultivo')
# st.title('Desk Service Newe Seguros')
st.title(':green[Cadastrar Cultivo]')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
with st.container():    
    # recebendo os dados para montar o relatório
    st.write('---')
    server = st.selectbox(':green[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
    IdFrutaGrao = st.text_input(":green[Digite o IdFrutaGrao:] ").strip()
    nome_cultivo = st.text_input(":green[Digite o nome do cultivo:] ").strip()

with st.spinner('Wait for it...'):        
    if st.button('inserir'):
        resultado = ro.executar_processo(server,IdFrutaGrao,nome_cultivo)
        if not resultado['erro']:
            if resultado['registrado']:
                st.warning('Produto já está registrado',icon="🚨")
            else:
                st.success('Registro feito com sucesso!')
                resultado['df']
            ro.config_log(server)    
        else:
            st.error('Seu produto não está cadastrado no SIP!',icon='🚨')

                
        
        
