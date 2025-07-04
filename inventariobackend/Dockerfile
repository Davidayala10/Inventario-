# Usa una imagen base oficial de Python
FROM python:3.11

# 🔧 Instala postgresql-client (para pg_isready)
RUN apt-get update && apt-get install -y postgresql-client

# Establece el directorio de trabajo en el contenedor
WORKDIR /opt

# Copia los archivos del proyecto al contenedor
COPY entrypoint.sh /opt/entrypoint.sh
COPY requirements.txt /opt/requirements.txt
COPY . .

# Instala las dependencias con mayor timeout y mirror alternativo (para evitar errores de red)
RUN pip install --no-cache-dir --timeout=120 -i https://pypi.org/simple/ -r requirements.txt

# Da permisos de ejecución al archivo entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /opt/entrypoint.sh

# Expone el puerto 8000 para la aplicación Django
EXPOSE 8000

# Ejecuta el script de entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]

# Comando por defecto para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
