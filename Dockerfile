# Start from Ubuntu 23.04 base image
FROM ubuntu:24.04 AS base

ARG GIT_REPO_URL
LABEL GIT_REPO_URL=${GIT_REPO_URL}

# Install necessary packages
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
    python3-venv \
    python3-pip \
    gcc \
    libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment and install dependencies
RUN python3 -m venv /venv
COPY requirements.txt /tmp/requirements.txt
RUN /venv/bin/pip install --upgrade pip setuptools wheel && \
    /venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Fix security vulnerabilities
RUN /venv/bin/pip install --upgrade --no-cache-dir starlette


## Main service ###
FROM base AS server
COPY --from=base /venv /venv
# COPY ./requirements.txt /tmp/requirements.txt
# RUN /venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Copy your application code
COPY ./engine /app/engine
COPY ./tests /app/tests

# Set the working directory
WORKDIR /app
CMD ["/venv/bin/fastapi", "run", "engine/main.py","--port","8001"]