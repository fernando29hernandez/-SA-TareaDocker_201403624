from typing import List, Dict  # import del manejo de listas
from flask import Flask  # import para el funcionamiento general de flask
import mysql.connector  # import de conexion con mysql
import json  # import para el manejo de variables tipo json

app = Flask(__name__)  # creacion de la app en python de flask


def estudiante() -> List[Dict]:
    # Variable utilizada para la conexion con la base de datos
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'TAREA_SA_201403624'
    }
    # variable de la conexion con la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    # ejecucion de consulta hacia la base de datos
    cursor.execute('SELECT * FROM estudiante')
    # creacion de objeto donde se almacenara el contenido de la tabla
    results = [{carne: nombre} for (carne, nombre) in cursor]
    # se cierra el cursor
    cursor.close()
    # se cierra tambien con la conexion hacia la BD
    connection.close()
    # retorno del objeto con el contenido de la tabla
    return results

# FUNCION de tipo get para mostrar los datos de la BD
@app.route('/')
def index() -> str:
    return json.dumps({'estudiantes': estudiante()})


if __name__ == '__main__':
    # comando para configurar la ip del servicio
    app.run(host='127.0.0.1')
