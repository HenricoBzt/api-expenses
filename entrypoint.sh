#!/bin/sh
# filepath: c:\Users\henri\OneDrive\Documentos\workspace\User_managment_api\entrypoint.sh


echo "Aguardando o banco de dados iniciar..."
while ! nc -z dpg-d1vdg1ndiees73bigqrg-a 5432; do
  sleep 1
done

echo "Executando migrações Alembic..."
alembic upgrade head


echo "Iniciando o servidor FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000