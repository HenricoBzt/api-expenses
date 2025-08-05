FROM python:3.12-slim
WORKDIR /app


COPY pyproject.toml .


RUN pip install --upgrade pip \
 && pip install --no-cache-dir . \
 && apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*


COPY . .
RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["sh", "/app/entrypoint.sh"]