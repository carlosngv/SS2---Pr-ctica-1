import pyodbc

host = 'localhost'
bd_name = 'ss2_practica1'
username = 'sa'
password = '7Dejunio'

try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' +
                              host + ';DATABASE=' + bd_name + ';UID=' + username + ';TrustServerCertificate=yes;PWD=' + password)
    print("Conexión exitosa")
    # OK! conexión exitosa
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)


"DRIVER={ODBC Driver 18 for SQL Server};SERVER=$url;DATABSE=$db;UID=$usr;TrustServerCertificate=yes;"
