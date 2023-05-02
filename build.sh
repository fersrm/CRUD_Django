#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Definir la variable de entorno para la URL de medios
export MEDIA_URL='/media/'

# Copiar los archivos de medios en la carpeta MEDIA_ROOT
python manage.py collectmedia --no-input
