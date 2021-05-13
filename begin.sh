#!/bin/bash

[[ -f "$1"  ]] || { echo "se espera como primer parametro un archivo .env"; exit 1; }

for linea in $(ccdecrypt -c "$1"); do
  echo "export $linea"
  export $linea
done

python manage.py runserver

