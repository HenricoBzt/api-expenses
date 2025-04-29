FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["sh", "/app/entrypoint.sh"]

