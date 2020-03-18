# creacion de imagen de python 
FROM python:3.6

EXPOSE 80
# Configuro la carpeta de trabajo
WORKDIR /app
# copia del archivo requeriments.txt a la carpeta app
COPY requirements.txt /app
# instalacion de los requeriemientos en la imagen
RUN pip install -r requirements.txt
# copia del archivo Server.py a la carpeta app
COPY Server.py /app
# configuracion del comando para correr la aplicacion
CMD python Server.py