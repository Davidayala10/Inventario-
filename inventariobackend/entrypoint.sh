#!/bin/bash

# Espera a que la base de datos esté lista
echo "Esperando a que PostgreSQL esté disponible..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL está listo. Aplicando migraciones..."
python manage.py migrate

echo "Iniciando el servidor Django..."
exec "$@"
