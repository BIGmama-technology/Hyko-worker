# Stage 1: Build stage for creating a venv with Poetry
FROM python:3.11.6-slim as poetry-builder

RUN apt update && \
    apt install -y --no-install-recommends git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Set poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 

RUN pip install poetry

COPY . .
RUN poetry install --no-cache

# Stage 2: Application stage for running the application using the venv
FROM python:3.11.6-slim as app-runner

RUN apt update && \
    apt install -y --no-install-recommends build-essential libgl1-mesa-glx libglib2.0-0 ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=poetry-builder /.venv /.venv
COPY ./src /src

# Activate the virtual environment
ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD arq src.remote_worker.WorkerSettings
