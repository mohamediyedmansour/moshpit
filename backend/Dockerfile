FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system moshpit \
    && adduser --system --ingroup moshpit moshpit

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* \
    && rm -rf /wheels

COPY app ./app
COPY gunicorn.conf.py .

RUN chown -R moshpit:moshpit /app

USER moshpit

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]

