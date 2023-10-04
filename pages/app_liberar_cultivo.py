import pandas as pd
import streamlit as st
import backend.liberar_cultivo_V2 as ro
import openpyxl as p
from time import sleep
from streamlit_extras.app_logo import add_logo

cont=2

util_global={}
def set_dict(dic):
    return dic

def verificar_cnpj(cnpj):
    if cnpj=='' or cnpj==None:
        st.error(':red[ERRO: Sem campo preenchido]', icon='🚨')
        return False
    else:
        cnpj.strip().replace('-','').replace('.','').replace('/','')
        if not cnpj.isdigit():
            st.error(':red[ERRO: Existe algum item que não é numérico]', icon='🚨')
            return False
        elif len(cnpj)>14 or len(cnpj)<1:
            st.error(':red[ERRO: Quantidade de dígitos]', icon='🚨')
            return False
        return True


st.set_page_config(page_title='Liberar Cultivo')
# st.title('Desk Service Newe Seguros')
st.title(':green[Liberar Cultivo]')

add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
with st.container():    
    # recebendo os dados para montar o relatório
    st.write('---')
    server = st.selectbox('Escolha o server: ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
    cnpj = st.text_input("Digite o CNPJ (Apenas os dígitos, sem ' - ' ou ' . ' ): ").strip()
    IdFrutaGrao = st.text_input('Digite o IdFrutaGrao: ').strip()
    

with st.spinner('Wait for it...'):        
    if st.button('Atualizar'):
        if verificar_cnpj(cnpj):       
            st.write('---')
            uteis=ro.executar_processo1(server, cnpj)
            util_global=set_dict(uteis)
            uteis2=ro.executar_processo2(server,IdFrutaGrao,util_global['cultivos_liberados'])
            st.subheader('Cultivos liberados para corretora atualmente')
            uteis['df1']
            st.subheader('Nome dos cultivos')
            uteis['df2']  
            st.write('---')
            st.write('Cultivo que será liberado: ')
            uteis2['df1']   
            cont=3


# with st.spinner('Wait for it...'):
            # resp=st.selectbox('Deseja atualizar',('Não','Sim'))
            # if st.button(':green[Confirmar]') and resp=='Sim':        
                # Atualizar
            if uteis2['atualiza']:     
                df_atualizado=ro.atualizar(server,uteis2['cultivos_liberados_novo'],util_global['corretora_id'],cnpj)
                st.success("Cultivo liberado!")
                #Mostrar Atualizado
                df_atualizado
            else:
                st.warning('O cultivo já está liberado!',icon='⚠️')
            ro.config_log(server)    
            # else:
            # st.warning('Selecione primeiro o campo visualizar!',icon='⚠️')            
            
        
