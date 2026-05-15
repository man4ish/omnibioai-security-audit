FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    "redis[asyncio]" \
    pydantic

COPY . .

EXPOSE 8004

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8004"]
