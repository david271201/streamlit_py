import streamlit_authenticator as stauth

aceito=False
acesso = {
          'teste_dev_1':'Dev@01',
          'teste_dev_2':'Dev@02',
          'teste_qas_1': 'QAS@01',
          'teste_qas_2' : 'QAS@02'          
          }

hashed = stauth.Hasher(['Dev@01','Dev@02']).generate()
print(hashed)


