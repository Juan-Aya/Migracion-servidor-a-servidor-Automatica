import pymysql
import conecciondb as con
import pandas as pd
from datetime import datetime


def insert_info(tb_origen,base_origen,tb_destino,campo_creacion):
    #Verificar si la tabla de destino tiene información 
    query = f"SELECT MAX({campo_creacion}) FROM {tb_destino};"
    try:
        conx_destino = con.cnnx_destino()
        cursor_destino = conx_destino.cursor()
        cursor_destino.execute(query)
        resultado = cursor_destino.fetchone()[0]
        conx_destino.close()
        cursor_destino.close
    except Exception as e:
        print(f'Error: al ejecutar la query: {e}.')
        conx_destino.close()
        cursor_destino.close

    if resultado:
        pass
        print('Informacion ya esta no hay nesecidad de insertarla toda.')
    else:
        # Obtener datos de la tabla de origen
        consulta_select_origen = f"SELECT * FROM {tb_origen};"
        try:
            conx_origen = con.cnnx_origen()
            cursor_origen = conx_origen.cursor()
            cursor_origen.execute(consulta_select_origen)
            datos_origen = cursor_origen.fetchall()
            conx_origen.close()
            cursor_origen.close()
        except Exception as e:
            print(f'Error: al ejecuta la query: {e}.')
            conx_origen.close()
            cursor_origen.close()

        # Obtener estructura de la tabla de origen
        consulta_columnas_origen = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
        """
        cursor_origen.execute(consulta_columnas_origen,(base_origen,tb_origen))
        columnas_origen = [column[0] for column in cursor_origen.fetchall()]

        # Construir consulta de inserción
        columnas_insert = ', '.join(columnas_origen)
        placeholders = ', '.join(['%s'] * len(columnas_origen))
        consulta_insert_destino = f"INSERT INTO {tb_destino} ({columnas_insert}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {', '.join([f'{col} = VALUES({col})' for col in columnas_origen])};"
        try:
            conx_destino = con.cnnx_destino()
            cursor_destino = conx_destino.cursor()

            # Insertar los datos en la tabla de destino usando executemany
            cursor_destino.executemany(consulta_insert_destino, datos_origen)
            # Confirmar los cambios y cerrar conexiones
            conx_destino.commit()
            
            conx_destino.close()
            cursor_destino.close
        except Exception as e:
            print(f'Error: al ejecutar la query: {e}.')
        conx_origen.close()
        conx_destino.close()
