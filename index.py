import os
import sys

def isRunningFromEXE():
    try:
        return getattr(sys, 'frozen', False)
    except:
        return False

def getPath():
    if isRunningFromEXE():
        getSctiptPath = os.path.abspath(sys.executable)
    else:
        getSctiptPath = os.path.abspath(__file__)
    scriptPath = os.path.dirname(getSctiptPath)
    return scriptPath

customPath = os.path.join(getPath(),'venv','Lib','site-packages')
sys.path.insert(0, customPath)

# Construye la ruta al archivo "config.json" en el mismo directorio que el script
scripts = os.path.join(os.path.dirname(os.path.abspath(__file__)),"scripts")
sys.path.insert(0, scripts)

import pymysql 
import json
import EncrDecr
import createdb
import modify_db
import insert_info
import update_info

with open("config.json", "r") as f:
  connection_params = json.load(f)

connection_params_ori = connection_params["origen"]
database_ori = EncrDecr.DeCrypt(connection_params_ori["database"]).strip("'")

connection_params_dest = connection_params["Destino"]
database_dest = EncrDecr.DeCrypt(connection_params_dest["database"]).strip("'")

#print(connection_params)       
tabla =  connection_params["Tablas"].keys()
tabla0 =  connection_params["Tablas"]

for i in range(len(list(tabla))):
    try:
        key = list(tabla)[i].strip("'")
        tabla_ori = list(tabla)[i].strip("'")
        campo_registro = tabla0[key][0].strip("'")
        campo_modify = tabla0[key][1].strip("'")
        tabla_dest = tabla0[key][2].strip("'")
        print(f'la clave es {list(tabla)[i]}, fecha1 {tabla0[key][0]}, fecha2 {tabla0[key][1]}')
        createdb.crear_tabla_destino(database_ori, tabla_ori, database_dest, tabla_dest)
        modify_db.comparacion_tablas(database_ori, database_dest, tabla_ori, tabla_dest)
        insert_info.insert_info(tabla_ori, database_ori, tabla_dest, campo_registro)
        update_info.update_info(database_ori, tabla_ori, tabla_dest, campo_modify)
        print(list(tabla)[i])
    except Exception as e:
        print(f"Error al procesar la tabla '{list(tabla)[i]}': {e}")
        continue


    
