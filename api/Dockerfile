# Multi-stage build para API Python

# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Run
FROM python:3.11-slim

WORKDIR /app

# Crear usuario no root
RUN groupadd -r pythonuser && useradd -r -g pythonuser pythonuser

# Copiar dependencias desde builder
COPY --from=builder /root/.local /root/.local

# Copiar código fuente
COPY --chown=pythonuser:pythonuser src ./src

ENV PATH=/root/.local/bin:$PATH

USER pythonuser

EXPOSE 3000

CMD ["python", "src/app.py"]
