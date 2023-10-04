import pandas as pd
import streamlit as st
import backend.Ajustar_Favorecido_V2 as ro
import openpyxl as p
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title='Ajustar Favorecido')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
# st.title('Desck Service Newe Seguros')

st.title(':green[Ajustar Favorecido]')

def verificar_cnpj(cnpj):
    if cnpj=='' or cnpj==None:
        st.error(':red[ERRO: Insira algum CPF/CNPJ válido]', icon='🚨')
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

with st.container():
    # recebendo os dados para montar o relatório
    server = st.selectbox(':green[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
    cd_apolice = st.number_input(':green[Digite o nome codigo da apólice / proposta]', format='%d', min_value=0)
    nr_endosso = st.selectbox(':green[Digite o número do endosso:] ',(0,1,2,3,4))
    cpf_cnpj = st.text_input(":green[Digite número de cpf do novo favorecido:] ").strip()
    codigo = st.selectbox(':green[informe Papel:]',options=('subvenção federal', 'subvenção estadual', 'segurado', 'beneficiário(Favorecido)'))
    if codigo == 'subvenção federal':
        papel=33
    elif codigo == 'subvenção estadual':
        papel=34
    elif codigo == 'segurado':
        papel=2
    elif codigo=='beneficiário(Favorecido)':
        papel=4

with st.spinner('Wait for it...'):        
    if st.button('Atualizar valores'): 
        if verificar_cnpj(cpf_cnpj):
            df=ro.executar_processo(server, cd_apolice, nr_endosso, papel, cpf_cnpj)
            st.success('Banco atualizado')
            df
            ro.definir_log(server)
        else:
            st.error('Erro ao atualizar')  
        ro.definir_log(server)    


            







