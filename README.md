
Automatización de migración de información de servidor a servidor //////////////////////////////////////////////////////////////////////

Este proyecto automatiza la migración de información de tablas de un servidor a otro. Para ello, realiza las siguientes validaciones para garantizar que la información sea correcta y efectiva en el destino:

    *) Verifica si la tabla destino existe en el servidor destino. Si no existe, la crea automáticamente con los mismos tipos de datos que la tabla origen. Además, asigna la primera columna de la tabla origen como clave principal en la tabla destino.

    *) Valida la estructura de las tablas de los dos servidores. Si encuentra diferencias, crea o elimina columnas en la tabla destino para que tenga la misma estructura que la tabla origen.

    *) Verifica si la tabla destino tiene datos. Si tiene datos, imprime un mensaje indicando que no es necesario migrar toda la información. Si no tiene datos, realiza una consulta a la tabla origen para obtener todos los datos y migrarlos a la tabla destino.

    *) Valida la columna de fecha de modificación en la tabla origen. Si existe, consulta la fecha de modificación más reciente en la tabla destino. Luego, realiza una consulta a la tabla origen para obtener todos los datos con una fecha de modificación igual o posterior a la fecha de modificación más reciente en la tabla destino. Estos datos se migran a la tabla destino.

Este proceso cuenta con una seguridad de información al encriptar los datos de origen y destino, así como los parámetros de conexión a los servidores de destino y origen.

Requisitos //////////////////////////////////////////////////////////////////////

El proceso requiere los siguientes datos, que se almacenan en un archivo JSON:

    *) Parámetros de conexión a los servidores de destino y origen
    *) Nombres de las tablas origen y destino
    *) Fechas de creación de las tablas origen y destino
    *) Fechas de modificación de las tablas origen y destino
Una vez que se han llenado estos requisitos, el proceso se ejecuta automáticamente y realiza todo el procedimiento descrito anteriormente.

Instrucciones de uso //////////////////////////////////////////////////////////////////////

Para utilizar este proyecto, siga los siguientes pasos:
    *) Cree un archivo JSON con los datos requeridos.
    *) Ejecute el comando python3 index.py

Ejemplo de archivo JSON:

{
    "origen": {
        "host": "5A6D526D416D5A6C5A78486D416D5A6A5A78486D416D57535A6D566D5A6A3D3D",
        "port": 3306,
        "user": "416D703241774D5241484C335A77706A4177523D",
        "password": "416D703241774D5241484C335A77706A4177526D5A775A6A5A6D566D5A743D3D",
        "database": "417744325A77706A41484C33416D4C344177523341514954417752325A474C6B41784C3241743D3D"
    },
    "Destino": {
        "host": "5A6D526D416D5A6C5A78486D416D5A6A5A78486D416D57535A6D4C6D5A4E3D3D",
        "port": 3306,
        "user": "4178523341474C6B417848325A4770354177526D41775A315A6D746D5A743D3D",
        "password": "5A6D526C446D714F41775A3245514C6C5A6D4E315A514432416D4E315A474C304152566D5A51494F5A6D78314147454F41774C325A6A3D3D",
        "database": "417756325A774C304177443145774C33416D563245777031416D4E325A6D4D54416D5A314577706C417748335A514D54416D5A324247703041784C335A774C3541784C314577706C416D4E325A443D3D"
    },
    "Tablas":{  
        "tabla_origen":["Fecha_regitro","Fecha_modificacion","tabla_destino"],
        "tabla_origen2":["Fecha_regitro","Fecha_modificacion","tabla_destino2"],
        - cunatas mas desee
        "tabla_origen3":["Fecha_regitro","Fecha_modificacion","tabla_destino3"]
        

    }
}

Explicación de los campos del archivo JSON //////////////////////////////////////////////////////////////////////

servidor_origen y servidor_destino: Datos de conexión a los servidores de origen y destino.
tablas: Nombres de las tablas origen y destino.
fechas: Fechas de creación y modificación de las tablas origen y destino.