FROM python:3.11-slim

# чтобы логи сразу писались в stdout
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# сначала зависимости (кеш Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем код приложения
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
