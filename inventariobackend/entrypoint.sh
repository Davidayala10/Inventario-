#!/bin/sh

echo "Esperando a que PostgreSQL esté disponible..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL está listo. Aplicando migraciones..."
python manage.py migrate

echo "Poblando la base de datos con datos sintéticos..."
python manage.py populate_data

echo "Iniciando el servidor Django..."
exec "$@"
