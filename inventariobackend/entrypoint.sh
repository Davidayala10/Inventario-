#!/bin/bash

echo "Esperando a que PostgreSQL esté disponible..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  echo "PostgreSQL no está listo aún. Esperando..."
  sleep 2
done

echo "PostgreSQL está listo. Aplicando migraciones..."
python manage.py migrate

echo "Verificando si ya existen datos..."
EXISTING_DATA=$(python manage.py shell -c "from api.models import DimCategoria; print(DimCategoria.objects.count())")

if [ "$EXISTING_DATA" = "0" ]; then
    echo "Poblando la base de datos con datos sintéticos..."
    python manage.py populate_data
else
    echo "Los datos ya existen, saltando la población de datos."
fi

echo "Iniciando el servidor Django..."
exec "$@"