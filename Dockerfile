# Start from Python 3.10-slim base image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# # Install necessary packages
# RUN apt-get update && \
#     apt-get install --no-install-recommends --yes \
#     gcc \
#     libpython3-dev \
#     && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy your application code
COPY ./engine /app/engine
COPY configuration.yaml /app/configuration.yaml

# Set the working directory
WORKDIR /app
CMD ["fastapi", "run", "engine/main.py","--port","8001"]
