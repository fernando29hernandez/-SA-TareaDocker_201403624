# creacion de imagen de python 
FROM python:3.6

EXPOSE 80
# Configuro la carpeta de trabajo
WORKDIR /app
# copia todos los archivos a la carpeta app para la instalacion de flask y el conector y paso del proyecto
ADD . /app
# instalacion de los requeriemientos en la imagen
RUN pip install -r ./app/requirements.txt
# configuracion del comando para correr la aplicacion
CMD python ./app/Server.py