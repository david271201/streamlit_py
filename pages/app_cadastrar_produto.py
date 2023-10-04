import pandas as pd
import streamlit as st
import backend.cadastrar_produto_V2 as ro
import openpyxl as p
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title='Ajustar Pagador')
# st.title('Desk Service Newe Seguros')
st.subheader(':green[Cadastrar Produto]')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
st.warning('É necessário que sejam preenchidos todos os campos para efetuar o cadastro!')


#Parte 1
with st.container():

    st.markdown('## Inserir Produto')

    #input usuario
    server = st.selectbox(':green[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))

    cod_prod=st.number_input(':green[Digite o código do produto:] ', min_value=0, format='%d')

    cod_ale=st.number_input(':green[Digite o código do NumeroProdutoPlanilha: ] ', min_value=0, format='%d')
    
    # executar backend
    with st.spinner('Wait for it...'):     
        if st.button('Inserir Produto'):   
            retornos1,continuar=ro.executar_processo1(server,cod_prod)
            retornos1['df1']
            # Tratativas para erros de cadastro
            if not continuar:
                st.error('Produto não cadastrado na I4pro')
                st.experimental_rerun()
            retornos1['df2']

            if retornos1['cadastrado']:
                st.warning('Seu produto já estava cadastrado no SIP')
                inserir1={}
                inserir1['df']=retornos1['df']
                inserir1['id_prod_plan']=retornos1['id_prod_plan']
                inserir1['continuar']=retornos1['continuar']
                proximo1=True
            else:
                inserir1=ro.inserir1(server,cod_ale,retornos1['nome_prod'],cod_prod)
                if not inserir1['continuar']:
                    st.error('Erro ao inserir produto!')
                    st.experimental_rerun()
                st.success(':green[Produto inserido com sucesso!]')
                inserir1['df']
                proximo1=True
    

# Parte 2
with st.container():
    proximo2=False
    percentuais=[]
    st.markdown('## Inserir Cobertura')
    #Executar para receber nomes e ids
    retornos2=ro.executar_processo2(server, cod_prod, inserir1['id_prod_plan'])    
    retornos2['df1']
    #verificando se já existe no sip
    #COLOCAR O NOT QUANDO ACABAR DE TESTAR
    if  retornos2['cadastrado']:
        #estabelecendo parametros para inserir a cobertura
        basica=st.selectbox('Escolha a básica: ',retornos2['col_nm_comercial'])
        for i,nome in enumerate(retornos2['col_nm_comercial']):
            if nome==basica:
                id_basica=i
        for i,nome in enumerate(retornos2['col_nm_comercial']):
            percentual=st.number_input(f"Qual o percentual de '{nome}' : ",min_value=0. ,format='%.2f',step=0.01)
            if not percentual:
                st.stop()    
            percentuais.append(percentual)
        with st.spinner('Wait for it...'):
            if st.button(':green[Inserir Cobertura]'):
                #atualizar
                inserir2=ro.inserir2(server,retornos2['col_id_produto_cobertura'] ,percentuais,retornos2['col_nm_comercial'],id_basica,inserir1['id_prod_plan'])
                inserir2['df']
                if not inserir2['continuar']:
                    st.error('Erro ao inserir cobertura!')
                    st.experimental_rerun()
                st.success('Cobertura foi inserida com sucesso!')
                proximo2=True
    else:
        st.warning('Cobertura já cadastrada no SIP')
        inserir2={}
        inserir2['df']=retornos2['df']
        inserir2['continuar']=retornos2['continuar']=True
        inserir2['col_id_cobertura_planilha']=retornos2['col_id_cobertura_planilha']
        inserir2['id_cobertura_planilha_basica']=retornos2['id_cobertura_planilha_basica']
        inserir2['df']
        proximo2=True


# Parte 3
with st.container():
    st.markdown('## Inserir Opções de Cobertura')
    if ro.executar_processo3(server,inserir2['id_cobertura_planilha_basica'],cod_prod):
        if len(retornos2['col_id_produto_cobertura']):
            comando=f"insert into OpcoesCobertura values (inserir2{'id_cobertura_planilha_basica'},NULL,NULL,NULL,NULL,1)"
            st.write(comando)
            # bo.execute_query(server_sip,database_sip,comando,persistence=True)
        else:
            qtd=st.text_input("Digite quantos insert irá fazer em OpcoesCobertura values: ") 
            qtd.strip()   
            if qtd =='' or qtd==None:
                st.stop()
            for i in range(qtd):
                ...
                #Pensar em como montar isso pro usuário    
    else:
        st.warning("Opção de cobertura já cadastrada no SIP")  


#Parte 4

#Parte 5
with st.container():
    cadastrado,retornos5=ro.executar_processo5(server,)
    
    if retornos5['cadastrado']:
        if not cadastrado:
            retornos5['df1']
            retornos5['df2']
            if st.button(':green[Inserir perguntas]'):
                inserir5=ro.inserir5(server,retornos5['lista_id_perg'],retornos5['lista_nm_perg'],retornos5['tupla_lista_id_perg'])
                if inserir5['cadastrado']:
                    st.success('Perguntas inseridas com sucesso!')
                    inserir5['df']
                else:
                    st.error('Erro ao inserir produto!') 
                    st.experimental_rerun()   
            else:
                st.stop()    
        else:
            retornos5['df3']
            st.warning('Perguntas já cadastradas na I4pro!')    
    else:
        st.error("Perguntas não cadastradas na I4pro!")
        st.experimental_rerun()

#Parte 6
with st.container():
    retornos6=ro.executar_processo6(server,inserir1['id_prod_plan'])
    if not retornos6['cadastrado']:
        inserir6=ro.inserir6(server,retornos5['lista_id_perg'],inserir1['id_prod_plan'])
        if inserir6['cadastrado']:
            st.success('Questionário cadastrado com sucesso! ')
            inserir6['df']
        else:
            st.error('Erro ao inserir produto!')
            st.experimental_rerun()    
    else:
        st.warning('Questionário já cadastrado!')
        retornos6['df']    
         
