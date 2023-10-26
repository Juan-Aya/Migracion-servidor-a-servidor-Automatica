import sys
import json
import pymysql
import EncrDecr
import os 

#//// FUNCIONES DE CONEXIONES A LAS DOS BASES DE DATOS ORIGEN Y DESTINO ////# 
    # Se requieren los siguientes datos:
    # Datos de conexión: host, port, user, password, database.

# Obtén la ruta del directorio actual del script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta al archivo "config.json" en el mismo directorio que el script
ruta_config_json = os.path.join(directorio_actual,'..',"config.json")

def cnnx_origen():
   with open(ruta_config_json, "r") as f:
    connection_params = json.load(f)
    
   connection_params = connection_params["origen"]
   conn_origen = pymysql.connect(host = EncrDecr.DeCrypt(connection_params["host"]),
                                 port = connection_params["port"],
                                 user = EncrDecr.DeCrypt(connection_params["user"]),
                                 passwd = EncrDecr.DeCrypt(connection_params["password"]),
                                database = EncrDecr.DeCrypt(connection_params["database"]))
   return conn_origen

   
def cnnx_destino():
   with open(ruta_config_json, "r") as f:
    connection_params = json.load(f)
   connection_params = connection_params["Destino"]
   conn_destino = pymysql.connect(host = EncrDecr.DeCrypt(connection_params["host"]),
                                 port = connection_params["port"],
                                 user = EncrDecr.DeCrypt(connection_params["user"]),
                                 passwd = EncrDecr.DeCrypt(connection_params["password"]),
                                database = EncrDecr.DeCrypt(connection_params["database"]))
   return conn_destino


