FROM python:3.11-slim-buster AS content-base

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements-api.txt ./

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements-api.txt

COPY src /app

RUN groupadd -r zara-fetcher && useradd -r -m -g zara-fetcher zara-fetcher
RUN chown -R zara-fetcher:zara-fetcher /app
USER zara-fetcher

ENTRYPOINT ["python", "api.py"]