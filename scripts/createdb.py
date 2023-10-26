import pymysql 
import conecciondb as con

#//// FUNCIÓN PARA CREAR LA NUEVA TABLA PARA COS BI ////#
    # La funcion requiere: 
    # Base de datos origen, Base de datos destino.
    # Tabla origen, Tabla destino.

def crear_tabla_destino(database_orig,table_orig,database_dest,table_dest):

    # Verifica si la tabla de destino ya existe

    consulta_existe_tabla = f"SHOW TABLES IN {database_dest} LIKE '{table_dest}'"
    try:
        conn_des = con.cnnx_destino()
        cursor_destino = conn_des.cursor()
        cursor_destino.execute(consulta_existe_tabla)
        cursor_destino.close
        conn_des.close()
    except Exception as e:
        print(f'Error al ejecutar la query: {e}.')
        cursor_destino.close
        conn_des.close()

    if cursor_destino.fetchone():

        print(f"La tabla '{table_dest}' ya existe en la base de datos destino. No es necesario crearla.")

    else:

        # Define la consulta SQL para obtener la estructura de la tabla original
        consulta_sql = """
            SELECT column_name, 
                CASE 
                    WHEN data_type = 'varchar' THEN 'varchar(320)' 
                    ELSE data_type 
                END AS data_type
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position;
        """ # sql_injeccion
        try:
            conn_ori = con.cnnx_origen()
            cursor_origen = conn_ori.cursor()
            # Ejecuta la consulta
            cursor_origen.execute(consulta_sql, (database_orig, table_orig))
            # Obtiene los resultados de la consulta
            resultados = cursor_origen.fetchall()

            conn_ori.close()
            cursor_origen.close()
        except Exception as e:
            print(f'error el ejcutar la consulta: {e}.')
            conn_ori.close()
            cursor_origen.close()

        if resultados:
            # Crea una nueva tabla en el servidor de destino con la estructura de la tabla original
            nombre_nueva_tabla = table_dest  # Usa el mismo nombre que la tabla de origen
            crear_tabla_sql = f"CREATE TABLE {nombre_nueva_tabla} ("

            # Agrega la columna de la clave primaria y el resto de las columnas
            columna_primaria = resultados[0][0]  # Toma el nombre de la primera columna como clave primaria
            crear_tabla_sql += f"{columna_primaria} {resultados[0][1]} PRIMARY KEY, "

            # Itera a través de los resultados para construir la estructura de la nueva tabla, omitiendo la primera fila
            for fila in resultados[1:]:
                nombre_columna = fila[0]
                tipo_dato = fila[1]
                crear_tabla_sql += f"{nombre_columna} {tipo_dato}, "

            # Elimina la coma y el espacio finales
            crear_tabla_sql = crear_tabla_sql[:-2]

            # Cierra la declaración CREATE TABLE
            crear_tabla_sql += ")"

            try:
                conn_des = con.cnnx_destino()
                cursor_destino = conn_des.cursor()
                # Ejecuta la consulta para crear la nueva tabla
                cursor_destino.execute(crear_tabla_sql)
                conn_des.commit()
                cursor_destino.close
                conn_des.close()

            except Exception as e:
                print(f'Error: al ejecutar la query: {e}')
                cursor_destino.close
                conn_des.close()

            print(f"Tabla '{nombre_nueva_tabla}' creada con éxito en la base de datos destino, con la primera columna como clave primaria y tipos de datos VARCHAR modificados.")
        else:
            print(f"No se encontraron resultados para la tabla '{table_orig}' en la base de datos origen.")