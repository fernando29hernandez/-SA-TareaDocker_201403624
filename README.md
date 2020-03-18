# Tarea No.6 del Laboratorio de Software Avanzado

## Fernando Antonio Hernadez Gramajo


## Aplicacion flask 

La aplicacion la cual vamos a dockerizar esta escrita en flask(python). Los metodos mas importantes de este son los siguientes:

### Conexion a bd y extraccion de datos
```sh 
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

```
### Servir la pagina web y renderizar contenido


```sh 
# FUNCION de tipo get para mostrar los datos de la BD
@app.route('/')
def index():
    return render_template("index.html", results=estudiante())

```
### intepretacion en html

Una vez en la renderizacion del sitio los datos se ingresan a un for el cual ira creando por cada elemento una nueva fila en la tabla

```sh
 <!-- TABLA DONDE SE MOSTRARAN LOS ESTUDIANTES-->
    <table id="customers">
        <tr>
            <th>Carne|Nombre</th>
            
        </tr>
        {% for estudiante in results %}
        <tr>
            <td>{{ estudiante|tojson }}</td>
            
        </tr>
        {% endfor %}

    </table>
```

## Archivo requeriments

Solo necesita indicar la version de flask y del conector de MySQL con python

```sh
Flask
mysql-connector
```

## Datos a cargar en MySQL

Los datos a cargar en mysql se encuentran en un archivo con el nombre init.sql en una carpeta con el nombre db la misma se le pasa como parametro de volumen de datos en el archivo docker-compose.yml

El contenido del archivo es el siguiente:

```sh
CREATE DATABASE TAREA_SA_201403624;
use TAREA_SA_201403624;

CREATE TABLE estudiante (
  carne VARCHAR(10),
  nombre VARCHAR(20)
);

INSERT INTO estudiante
  (carne, nombre)
VALUES
  ('201403624', 'Fernando'),
  ('201400968', 'Juan'),
  ('201085123', 'Pedro'),
  ('201396854', 'Pablo'),
  ('201196470', 'Jose'),
  ('201403625', 'Antonio'),
  ('200598741', 'Daniel'),
  ('200684177', 'Manuel'),
  ('201014478', 'Mario'),
  ('199963968', 'Carlos');

```


## Archivo Dockerfile

Este archivo se construye desde una imagen de python3.6 a la cual se le pasara y configurara todo lo necesario para el despligue de la aplicacion en flask y su conexion en mysql

El contenido del archivo es el siguiente:

```sh
# creacion de imagen de python 
FROM python:3.6
# Configuro la carpeta de trabajo
WORKDIR /app
# copia todos los archivos a la carpeta app para la instalacion de flask y el conector y paso del proyecto
ADD . /app
# instalacion de los requeriemientos en la imagen
RUN pip install -r ./app/requirements.txt
# configuracion del comando para correr la aplicacion
CMD python ./app/Server.py
```


## Archivo docker-compose.yml

Este es el archivo por el cual se hara el despligue de la aplicacion en conjunto con la base de datos, dado que es donde se crearan ambos contenedores enlazadolos para que existe comunicacion entre si y dejandolos ejecutarse en segundo plano, el siguiente archivo tiene las configuraciones de puertos, nombres de las aplicaciones y volumenes utilizados asi como si se necesitase de otra imagen de docker para el despligue en conjunto.


```sh
version: "2"
services:
  app:
    build: .
    links:
      - db
    ports:
      - "80:5000"      
  db:
    image: mysql:5.7
    ports:
      - "32000:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - ./db:/docker-entrypoint-initdb.d/:ro
```

- "version ‘2’": Los archivos docker-compose.yml son versionados, lo que significa que es muy importante indicar la version de las instrucciones que queremos darle. A medida de que Docker evoluciona, habrá nuevas versiones, pero de todos modos, siempre hay compatabilidad hacia atras, al indicar la version de la receta.

- "build .": Se utiliza para indicar donde está el Dockerfile que queremos utilizar para crear el contenedor. Al definier “.” automaticamente considerará el Dockerfile existente en directorio actual.

- "links": Se utiliza para indicar con que otro contenedor tendra comunicacion el contenedor actual.

- "environment": Se utiliza para definir variables de entorno, en este caso para la base de datos.

- "image": se utiliza para la creacion de un contenedor utilizando la imagen que se indique.

- "ports": Aqui mapeamos los puertos locales 3306 (MySQL) y 5000 (flask) al servidor host. Esto permitirá que accediendo a IP:80 podamos probar el sitio generador por flask.

- "volumes": Aqui hacemos que el directorio actual se mapee directamente con el /db, para que se utilice como datos en MySQL.

## Correr todo

Simplemente ubicando en la carpeta raiz de proyecto procedemos a abrir un terminal y escribir el comando.

```sh
docker-compose up -d
```
Nota:-d sirve para ejecute todo desde segundo plano sin necesidad de tener una terminal abierta.


## Video Demostracion de la aplicación

[![Ver en youtube](https://img.youtube.com/vi/2SQgWK9s-nw/1.jpg)](https://youtu.be/2SQgWK9s-nw)
