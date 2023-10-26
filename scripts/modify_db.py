import pymysql
import pandas as pd
import conecciondb as con

#//// FUNCIÓN PARA COMPARAR TABLAS QUE MANTENGAN LA MISMA EXTRUCTURA ////#
    # Requiere los siguiente:
    # Base de datos origen, Base dedatos destino.
    # Tabla origen, Tabla destino.   

def comparacion_tablas(base_ori,base_dest,tb_ori,tb_dest):

    # Define las consultas SQL para obtener la estructura de ambas tablas
    consulta_origen = """
    SELECT column_name, 
        CASE 
            WHEN data_type = 'varchar' THEN 'varchar(320)' 
            ELSE data_type 
        END AS data_type
    FROM information_schema.columns
    WHERE table_schema = %s AND table_name = %s
    ORDER BY ordinal_position;
    """

    consulta_destino = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = %s AND table_name = %s
    ORDER BY ordinal_position;
    """
    try:
        conexion_origen = con.cnnx_origen()
        cursor_origen = conexion_origen.cursor()

        # Ejecuta ambas consultas
        cursor_origen.execute(consulta_origen,(base_ori,tb_ori))
        # Obtiene los resultados de ambas consultas como DataFrames de Pandas
        df_origen = pd.DataFrame(cursor_origen.fetchall(), columns=['column_name', 'data_type'])

        conexion_origen.close()
        cursor_origen.close()
    except Exception as e:
        print(f'Error: al ejecutara la query {e}.')
    try:
        conexion_destino = con.cnnx_destino()
        cursor_destino = conexion_destino.cursor()

        cursor_destino.execute(consulta_destino,(base_dest,tb_dest)) 
        df_destino = pd.DataFrame(cursor_destino.fetchall(), columns=['column_name', 'data_type'])

        conexion_destino.close()
        cursor_destino.close()
    except Exception as e:
        print(f'Error: al ejecutar la query: {e}.')
        conexion_destino.close()
        cursor_destino.close()

    # Encuentra las diferencias utilizando la función isin de Pandas
    diferencias = df_origen[~df_origen['column_name'].isin(df_destino['column_name'])]

    # Si hay diferencias, agrega las columnas faltantes a la tabla de destino
    if not diferencias.empty:
        for index, row in diferencias.iterrows():
            columna = row['column_name']
            tipo_dato = row['data_type']
            alter_table_sql = f"ALTER TABLE {tb_dest} ADD COLUMN {columna} {tipo_dato};"
            try:
                conexion_destino = con.cnnx_destino()
                cursor_destino = conexion_destino.cursor()
                cursor_destino.execute(alter_table_sql)
                conexion_destino.close()
                cursor_destino.close()
            except Exception as e:
                print(f'Error: al ejecutar la query: {e}.')
                conexion_destino.close()
                cursor_destino.close()

            print(f'Columnas Agregadas: {columna}, {tipo_dato}.')

    # Validación adicional: eliminar columnas de destino que no están en origen
    columnas_a_eliminar = df_destino[~df_destino['column_name'].isin(df_origen['column_name'])]
    if not columnas_a_eliminar.empty:
        for index, row in columnas_a_eliminar.iterrows():
            columna_a_eliminar = row['column_name']
            alter_table_sql = f"ALTER TABLE {tb_dest} DROP COLUMN {columna_a_eliminar};"
            try:
                conexion_destino = con.cnnx_destino()
                cursor_destino = conexion_destino.cursor()
                cursor_destino.execute(alter_table_sql)        
                conexion_destino.close()
                cursor_destino.close()
            except Exception as e:
                print(f'Error: al ejecutar la query: {e}.') 
                conexion_destino.close()
                cursor_destino.close()
            print(f'Columnas Eliminadas: {columna_a_eliminar}.')

    print("Comparación y actualización de estructuras completada.")
