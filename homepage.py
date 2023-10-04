import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo
from credenciais import acesso
import os 
import subprocess

st.set_page_config(page_title='homepage', page_icon= "🤖")

login_credentials = acesso

# st.title('Desk Service Newe Seguros')
# image = Image.open('MicrosoftTeams-image (1).png')
# st.image(image)
st.sidebar.success('Selecione a execução acima.')

add_logo(r"C:\Users\david.souza\Downloads\logan_newe.png", height=150)
     
# Credenciais de acesso (exemplo básico)

st.title("Página de Login")
# Criar campos para entrada de usuário e senha
username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

diretorio_homepage = os.path.abspath(os.getcwd())
# Botão de login
if st.button("Login"):
    if username in login_credentials.keys() and password == login_credentials[username]:
        st.success("Login bem-sucedido!")
        with open(r'pages\cred.txt', 'w') as arquivo:
            arquivo.write('True')
        # Redirecionar para o script "homepage.py" após o login bem-sucedido
        # path=os.path.join(".","scripts_web")
        # os.chdir(path)
        # subprocess.run(["streamlit", "run", "homepage.py"])
    else:
        st.error("Credenciais inválidas. Tente novamente.")
