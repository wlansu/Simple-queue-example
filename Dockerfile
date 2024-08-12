# pull official base image
FROM python:3.12.4

# --- Install Poetry ---
ARG POETRY_VERSION=1.8

ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=0
ENV POETRY_VIRTUALENVS_CREATE=0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Install dependencies
RUN apt-get update && apt-get install -y \
    jq

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /usr/src/app

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . ./