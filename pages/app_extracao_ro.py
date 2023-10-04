import pandas as pd
import streamlit as st
import backend.Extracao_RO_V2 as ro
import openpyxl as p
from datetime import date
import io
import xlsxwriter
from streamlit_extras.app_logo import add_logo
# :open_file_folder: 
# :calendar:

hoje = str(date.today()).replace('-','')

st.set_page_config(page_title='Extração Relatório Oficial', layout='wide',page_icon= "🤖")
# st.header('Desck Service Newe Seguros')
st.title(':green[Extração de Relatório Oficial]')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
# ⚠️

def validar_data(data_inicio,data_final):
    if int(data_inicio)>int(data_final):
        st.error(""" :red[ERRO:] \n :red[Data inicial maior que data final!]""", icon="🚨")
        return False
    elif int(data_inicio)>int(hoje):
        st.error(""" :red[ERRO: 
                 Data incicial maior que data de hoje!]""", icon="🚨")
        return False
    elif int(data_final)>int(hoje):
        st.error(""" :red[ERRO: 
                 Data de final maior que data de hoje!]""", icon="🚨")
        return False
    elif not data_inicio:
        st.error(""":red[ERRO: 
                 Data inicial não preenchida!]""", icon="🚨")
        return False
    elif not data_final:
        st.error(""":red[ERRO: 
                 Data final não preenchida!]""", icon="🚨")
        return False
    return True

def data_padrao(data):
    data=str(data)
    data= data.split('-')
    ano=data[0]
    mes=data[1]
    dia=data[2]
    data_padrao=ano+mes+dia
    return data_padrao 

with st.container():
    server = st.selectbox(':green[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))
    data_inicio = st.date_input(label=':calendar: :green[Digite a data incial:] ', format = 'DD/MM/YYYY') 
    data_final = st.date_input(label=':calendar: :green[Digite a data final:] ', format = 'DD/MM/YYYY') 
    if data_inicio and data_final:
        data_inicio =data_padrao(data_inicio)
        data_final = data_padrao(data_final)
        nome_arquivo='Extracao_RO_' + str(data_inicio) +'_' + str(data_final) + ".xlsx"
    st.write('---')

with st.spinner('Wait for it...'):            
    if st.button(':open_file_folder: Gerar relatório'):
        if validar_data(data_inicio,data_final):
            with st.container():
                wb = p.Workbook()
                nome = f'C:\\Users\\david.souza\\python\\scripts_web\\{nome_arquivo}'
                wb.save(nome_arquivo)
                resultado = ro.montar_relatorio(data_inicio, data_final, nome_arquivo, server)
                ro.montar_arquivo(nome_arquivo, resultado)
                arquivo = pd.read_excel(nome_arquivo, sheet_name=None)  # Lê todas as abas do arquivo Excel em um dicionário de DataFrames

            # Codificar os dados do Excel como bytes e criar um objeto de arquivo simulado (file-like object)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in arquivo.items():  # Itera sobre cada DataFrame do dicionário
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
            excel_data = output.getvalue()

            # Exibir o botão de download após a geração do arquivo Excel
            with st.container():
                st.write('---')
                st.download_button(
                    label=":green[Baixar relatório]",
                    data=excel_data,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        