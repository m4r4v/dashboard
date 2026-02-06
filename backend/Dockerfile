# Base Oficial: Python 3.11 Slim (Debian Bookworm)
FROM python:3.11-slim

# Variables de Entorno: Deshabilitamos virtualenv para instalar en sistema (dentro del contenedor)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Agregamos Poetry al PATH del sistema
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalación de dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalación Oficial de Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Directorio de trabajo
WORKDIR /workspace

# CAPA DE CACHÉ: Copiamos definición de dependencias antes del código
COPY pyproject.toml poetry.lock ./

# Instalación de dependencias del proyecto
# FIX CRÍTICO: Ejecutamos 'poetry lock' para sincronizar el lockfile con el toml
# antes de instalar. Esto repara discrepancias causadas por ediciones manuales.
RUN poetry lock --no-update && poetry install --no-root --no-interaction --no-ansi

# Nota: El código fuente se montará vía volumen en docker-compose