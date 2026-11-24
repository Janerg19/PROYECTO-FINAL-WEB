# Build para API Python con gunicorn

FROM python:3.12-slim

WORKDIR /app

# Crear usuario no root
RUN groupadd -r pythonuser && useradd -r -g pythonuser pythonuser

# Copiar requirements primero para caché
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY --chown=pythonuser:pythonuser src ./src
COPY --chown=pythonuser:pythonuser wsgi.py ./

USER pythonuser

EXPOSE 3000

# Usar gunicorn en producción
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "--timeout", "120", "wsgi:app"]
