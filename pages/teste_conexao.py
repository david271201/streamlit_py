import pyodbc
import pandas as pd
import streamlit as st
import openpyxl as p
from datetime import date
from streamlit_extras.app_logo import add_logo


server = "gcpi4prodbdev01"
username = "python_sql_dev"
password = "Newe@2303"
database= "newe_erp_cli"


def testar(query, *args):  
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = connection.cursor()
    results = []  # Lista para armazenamento dos resultados junto os nomes de colunas
    try:
        cursor.execute(query, *args)
        columns = [column[0] for column in cursor.description]  # Capturando as colunas do dataset
        for row in cursor.fetchall():  # Para cada linha do resultado do banco, mesclar o resultado do banco junto ao nome da coluna.
            results.append(dict(zip(columns, row)))
            
        return results
    except Exception as error:
        raise Exception('Erro ao executar a query "{}" \n \n ERRO: {}'.format(query, error))
    finally:
        cursor.close()
        connection.close()

# hoje = str(date.today()).replace('-','')

st.set_page_config(page_title='Extração Relatório Oficial', layout='wide',page_icon= "🤖")
# st.header('Desck Service Newe Seguros')
st.title(':green[Teste Conexão]')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
 
st.header("Testando")

cd_apolice=123
nr_endosso=1

with st.spinner('Wait for it...'):    
    comando = f"""Select ce.id_endosso, ce.nr_endosso, ce.vl_total
    from corp_endosso ce
    join corp_sub_estipulante csb on csb.id_sub = ce.id_sub
    join corp_apolice ca on ca.id_apolice = csb.id_apolice
    where ca.cd_apolice = {cd_apolice} and ce.nr_endosso = {nr_endosso}"""

    tabela = testar(server, database, username, password, comando)
    tabela = pd.DataFrame(tabela)
    tabela
    st.success('Deu certo :)')



       
