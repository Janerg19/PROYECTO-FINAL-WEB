# Build para API Python

FROM python:3.11-slim

WORKDIR /app

# Crear usuario no root
RUN groupadd -r pythonuser && useradd -r -g pythonuser pythonuser

# Copiar requirements primero para caché
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY --chown=pythonuser:pythonuser src ./src

USER pythonuser

EXPOSE 3000

CMD ["python", "src/app.py"]
