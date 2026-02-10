# ==============================================================================
# BACKEND DOCKERFILE - ARCHITECTURE V1.1.0
# ==============================================================================

# 1. IMAGEN BASE (Python 3.11 Slim)
FROM python:3.11-slim

# 2. VARIABLES DE ENTORNO
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Agregar Poetry y Venv al PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# 3. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA
# build-essential y libpq-dev son necesarios para compilar psycopg (asyncpg) y otras libs
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. INSTALACIÓN DE POETRY (RNF-04)
# Instalamos usando el script oficial para aislar dependencias de Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# 5. CONFIGURACIÓN DE USUARIO NON-ROOT (RNF-02)
# Creamos un grupo y usuario con UID 1000
RUN groupadd -g 1000 dashboard && \
    useradd -m -u 1000 -g dashboard -s /bin/bash dashboard

# 6. PREPARACIÓN DEL DIRECTORIO DE TRABAJO
WORKDIR /workspace

# Copiamos solo los archivos de dependencias para aprovechar el caché de Docker
COPY pyproject.toml poetry.lock* ./

# Instalamos dependencias (Nota: En desarrollo, docker-compose sobreescribe esto,
# pero es vital para construir la imagen base correctamente).
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# 7. PERMISOS FINALES
# Aseguramos que el usuario dashboard tenga control sobre el espacio de trabajo
RUN chown -R dashboard:dashboard /workspace

# 8. CAMBIO DE USUARIO (RNF-02)
USER dashboard

# El comando de arranque se delega al docker-compose.yaml