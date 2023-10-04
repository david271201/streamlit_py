import pyodbc
import logging
import datetime
import pyautogui
import logging
import nbformat


# Método que realiza a conexão no banco de dados
def db_connection(driver, server, database):
    """
    Establish a connection to a database using pyodbc lib
    :param driver: str
        database driver name
    :param server: str
        database server
    :param database: str
        database name
    :return: pyodbc connection object
    """
    try:
        connection = pyodbc.connect('Driver={}'.format(driver) +
                                    'Server={}'.format(server) +
                                    'Database={}'.format(database) +
                                    'Trusted Connection=yes;')
        if not connection:  # CASO NÃO HAJA CONEXÃO COM O BANCO DE DADOS
            print('Erro ao se conectar ao banco de dados')
    except Exception as error:
        print('Erro ao se conectar ao banco de dados: {}'.format(error))
        raise Exception('Erro ao se conectar ao banco de dados. \n \n {}'.format(error))
    return connection


def execute_query(server,database, query, params=None, many=False, persistence=False):
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;autocommit=True')
    cursor = connection.cursor()
    try:
        if many is False:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
        else:
            cursor.fast_executemany = True
            cursor.executemany(query, params)

        if persistence:
            cursor.commit()
            if cursor.rowcount > 1:
                logging.info('Affected rows: {}'.format(cursor.rowcount))
    except pyodbc.IntegrityError as ie:
        logging.error('An integrity error has occurred.', exc_info=True)
        raise ie
    except Exception as e:
        logging.error("Error while running a query execution: {}".format(e))
        raise Exception("Error while running a query execution: {}".format(e))
    finally:
        cursor.close()


def get_single_result(connection, query, *args):
    """
    Método que retorna um resultado único do banco.
    :param connection: pyodbc connection obj
    :param query: str
    :param args: tuple
    :return: dataset
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, *args)
        dados = cursor.fetchone()
        result = dados[0]
        return result
    except Exception as error:
        raise Exception('Erro ao executar a query "{}" \n \n ERRO: {}'.format(query, error))
    finally:
        cursor.close()


def get_multiple_result_sip(server, database,query, *args):
    """
    Método que retorna multiplos resultados do banco
    :param connection: pyodbc connection obj
    :param query: str
    :param args: tuple
    :return: dataset
    """

    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;autocommit=True')
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
    

def get_multiple_result_i4pro(server,database,query, *args):
    """
    Método que retorna multiplos resultados do banco
    :param connection: pyodbc connection obj
    :param query: str
    :param args: tuple
    :return: dataset

    """
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;autocommit=True')
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

def update(server,database,query,*args):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;autocommit=True')
        cursor = connection.cursor()
        cursor.execute(query,*args)
        cursor.commit()
    except Exception as error:
        raise Exception('Erro ao executar a query "{}" \n \n ERRO: {}'.format(query, error))
    finally:
        cursor.close()
        connection.close()


def show_logs(logs):
    for log in logs:
        print(log)       
        
def get_multiple_result(connection,query, *args):
    """
    Método que retorna multiplos resultados do banco
    :param connection: pyodbc connection obj
    :param query: str
    :param args: tuple
    :return: dataset
    """
    # server = 'gcpi4prodbdev01'
    # database = 'newe_erp_cli'
    # connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;autocommit=True')
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
        print('fechei em bo')

# Método que retorna o resultado de uma procedure do banco
def execute_proceudure(connection, query):
    no_count = 'SET NOCOUNT ON;'
    proc = no_count + query
    result = get_multiple_result(connection, proc)
    return result

def pegar_evidencia(i):
    imagem = pyautogui.screenshot()
    imagem.save(f'evidencia_{i}.png')
    



