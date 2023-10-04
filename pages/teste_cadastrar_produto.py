import pandas as pd
import streamlit as st
import backend.cadastrar_produto_V2 as ro
import openpyxl as p

# @st.cache_resource(experimental_allow_widgets=True)
def c1(estado):
    with st.container():
    # Parte 1
        passar=False
        st.markdown('## Inserir Produto')

        #input usuario
        server = st.selectbox(':violet[Escolha o server:] ',('gcpi4prodbdev01', 'gcpi4prodbprd01'))

        cod_prod=st.number_input(':violet[Digite o código do produto:] ', min_value=0, format='%d')

        cod_ale=st.number_input(':violet[Digite o código do NumeroProdutoPlanilha: ] ', min_value=0, format='%d')

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
                    passar=True
                else:
                    inserir1=ro.inserir1(server,cod_ale,retornos1['nome_prod'],cod_prod)
                    if not inserir1['continuar']:
                        st.error('Erro ao inserir produto!')
                        st.experimental_rerun()
                    st.success(':green[Produto inserido com sucesso!]')
                    inserir1['df']
                    proximo1=True
                    passar=True
                estado['c1']=True
                return server,cod_ale,cod_prod,inserir1
            else:
                st.stop()
                        


@st.cache(allow_output_mutation=True,suppress_st_warning=True)
def c2(estado,server,cod_prod,inserir1):
    
    with st.container():
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
                retornos2['col_nm_comercial']
                percentual=st.text_input(f"Qual o percentual de '{nome}' : ")    
                if percentual == None:
                    st.stop()
                percentuais.append(percentual)
            
            if st.button(':green[Inserir Cobertura]'):
                #atualizar
                inserir2=ro.inserir2(server,retornos2['col_id_produto_cobertura'] ,percentuais,retornos2['col_nm_comercial'],id_basica,inserir1['id_prod_plan'])
                inserir2['df']
                if not inserir2['continuar']:
                    st.error('Erro ao inserir cobertura!')
                    st.experimental_rerun()
                st.success('Cobertura foi inserida com sucesso!')
                proximo2=True
                estado['c2']=True
                return inserir2
            else:
                st.stop()
        else:
            st.warning('Cobertura já cadastrada no SIP')
            inserir2={}
            inserir2['df']=retornos2['df']
            inserir2['continuar']=retornos2['continuar']=True
            inserir2['col_id_cobertura_planilha']=retornos2['col_id_cobertura_planilha']
            inserir2['id_cobertura_planilha_basica']=retornos2['id_cobertura_planilha_basica']
            inserir2['df']
            estado['c2']=True
            return inserir2
            proximo2=True


def c3(estado,server,inserir2,cod_prod):
    with st.container():
        st.markdown('## Inserir Opções de Cobertura')
        if ro.executar_processo3(server,inserir2['id_cobertura_planilha_basica'],cod_prod):
            estado['c3']=True
            ...
            #caso dê certo terminar
        else:
            st.warning("Opção de cobertura já cadastrada no SIP")


def main():
    st.set_page_config(page_title='Ajustar Pagador')
    st.title('Desk Service Newe Seguros')
    st.subheader('Cadastrar Produto')
    st.warning('É necessário que sejm preenchidos todos os campos para efetuar o cadastro!')

    estado = st.session_state.get('estado',{'c1':False,'c2':False,'c3':False,'c4':False })

    server,cod_ale,cod_prod,inserir1=c1(estado)

    if estado['c1']:
        inserir2=c2(estado,server,cod_prod,inserir1)
    
    if estado['c2']:
        c3(estado,server,inserir2,cod_prod)

if __name__ == "__main__":
    main()
        
    










                
