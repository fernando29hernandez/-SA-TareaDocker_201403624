# creacion de imagen de python 
FROM python:3.6

EXPOSE 80
# Configuro la carpeta de trabajo
WORKDIR /app
# copia del archivo requeriments.txt a la carpeta app necesario para la instalacion de flask y el conector
COPY ./app /app
# instalacion de los requeriemientos en la imagen
RUN pip install -r app/requirements.txt
# configuracion del comando para correr la aplicacion
CMD python Server.py