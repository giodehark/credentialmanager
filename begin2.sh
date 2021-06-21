#!/bin/bash

[[ -f "$1"  ]] || { echo "se espera como primer parametro un archivo .env"; exit 1; }

for linea in $(ccdecrypt -c "$1"); do
  echo "export $linea"
  export $linea
done

clear
while :
do
  echo "Escoja una opción "
  echo "1. Iniciar el servidor"
  echo "2. Aplicar las migraciones: migrate"
  echo "3. Crear nueva migración: makemigration"
  echo "4. Salir del menú "
  echo -n "Debes seleccionar solo opciones del [1 al 4]"
  echo " "
  read opcion
  case $opcion in
    1)
      echo "Iniciando servidor...";
      python3 manage.py runserver;;
    2)
      echo "Aplicando migraciones...";
      python3 manage.py migrate;;
    3)
      echo "Creando nueva migración";
      python3 manage.py makemigrations;;
    4)
      break;;
    *) echo "$REPLY Es una opción inválida";
      ;;
    esac
   done