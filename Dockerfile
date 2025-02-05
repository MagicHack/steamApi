# syntax=docker/dockerfile:1


ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
    
# kinda hacky to force download of file since we check last update
RUN touch -d "24 hours ago" steam.json && \
    chown appuser:appuser steam.json

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY src .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD gunicorn --workers 3 --bind=0.0.0.0:8000 wsgi:app
