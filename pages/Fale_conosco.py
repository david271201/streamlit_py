import streamlit as st
import os
import smtplib
import win32com.client as win32
import pythoncom
from streamlit_extras.app_logo import add_logo
def mandar_email(corpo):
    try:
        pythoncom.CoInitialize()

        # Criar a integração com o outlook
        outlook = win32.Dispatch('outlook.application')

        # Criar um email
        email = outlook.CreateItem(0)

        # Configurar as informações do e-mail
        # email.To = "davs.david2001@gmail.com"
        email.To="jennifer.torres@neweseguros.com"
        email.Subject = "Problema com execução de automatção script"
        email.HTMLBody = f"""<b> Problema relatado:</b>
                            {corpo} """
        email.Send()
    except Exception as e:
        st.write("⚠️ Erro ao enviar email! ")
        st.error(f'ERRO: {e}',icon="🚨")


st.set_page_config(page_title='Ajustar Favorecido')
add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
# st.title('Desk Service Newe Seguros')
st.subheader('Como podemos te ajudar hoje?')
prompt = st.text_area(label='💭 Conte-nos o que aconteceu',placeholder="Escreva aqui").strip()
if prompt:
    mandar_email(prompt)
    st.write(':green[Mensagem enviada com sucesso]')
st.warning("⚠️ Aperte 'Crtl' + 'Enter' para enviar!")



