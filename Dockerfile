FROM python:3.9-slim as builder

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd -r botgroup && useradd -m -r -g botgroup botuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY . /app/
RUN chown -R botuser:botgroup /opt/venv /app

USER botuser

ENV PORT=8080

CMD ["gunicorn", "WebStreamer.server:web_server", "--bind", "0.0.0.0:$PORT", "--worker-class", "aiohttp.GunicornWebWorker"]
