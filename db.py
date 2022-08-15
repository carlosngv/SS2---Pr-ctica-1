import pyodbc

host = 'localhost'
bd_name = 'ss2_practica1'
username = 'sa'
password = 'TEST'

def connect_db():
    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + host + ';DATABASE=' + bd_name + ';UID=' + username + ';TrustServerCertificate=yes;PWD=' + password)
        return connection
    except Exception as e:
        print("An error has occured: ", e)
