import pymysql
import conecciondb as con

#//// FUNCIÓN PARA ACTUALIZAR INFORMACIÓN DE LA TABLA ////#
    # Solicita la siguiente info:
    # Base dedatos origen, Base de datos destino.
    # Tabla destino, Tabla origen.
    # Campo de fecha modificacion   

def update_info(base_origen,tb_origen,tb_destino,campo_modificacion): 
    
    query = f"SELECT MAX({campo_modificacion}) FROM {tb_destino} ;"

    try:
        conexion_destino = con.cnnx_destino()
        cursor_destino = conexion_destino.cursor()

        cursor_destino.execute(query)
        indicador = cursor_destino.fetchone()[0]

        conexion_destino.close()
        cursor_destino.close()
    except Exception as e:
        print(f'Error: al ejecutar la query {e}.')
        conexion_destino.close()
        cursor_destino.close()

    # Obtener datos de la tabla de origen
    consulta_select_origen = f"SELECT * FROM {tb_origen} WHERE {campo_modificacion} >= '{indicador}';"
    try:
        conexion_origen = con.cnnx_origen()
        cursor_origen = conexion_origen.cursor()

        cursor_origen.execute(consulta_select_origen)
        datos_origen = cursor_origen.fetchall()

        conexion_origen.close()
        cursor_origen.close()
        
    except Exception as e:
        print(f'Error: al ejecutar la query: {e}.')

    # Obtener estructura de la tabla de origen
    consulta_columnas_origen = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
    """
    try:
        conexion_origen = con.cnnx_origen()
        cursor_origen = conexion_origen.cursor()

        cursor_origen.execute(consulta_columnas_origen,(base_origen,tb_origen))
        columnas_origen = [column[0] for column in cursor_origen.fetchall()]

        conexion_origen.close()
        cursor_origen.close()

    except Exception as e:
        print(f'Error: al ejecutar la query: {e}.')
        conexion_origen.close()
        cursor_origen.close()

    # Construir consulta de inserción
    columnas_insert = ', '.join(columnas_origen)
    placeholders = ', '.join(['%s'] * len(columnas_origen))
    consulta_insert_destino = f"INSERT INTO {tb_destino} ({columnas_insert}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {', '.join([f'{col} = VALUES({col})' for col in columnas_origen])};"

    try:
        conexion_destino = con.cnnx_destino()
        cursor_destino = conexion_destino.cursor()    

        # Insertar los datos en la tabla de destino usando executemany
        cursor_destino.executemany(consulta_insert_destino, datos_origen)

        conexion_destino.commit()
        conexion_destino.close()
        cursor_destino.close()
    except Exception as e:
        print(f'Error: al ejecutar la quiery {e}.')
    print(f"Migración completada con idicador de: {indicador}.")