# Super Puper Tour Agency


## Запуск через Docker 

### 1) Подготовить .env

Создай файл `.env` рядом с `Dockerfile`:

```
APP_NAME=Super Puper Tour Agency
DEBUG=true
JWT_SECRET=super-secret-key
JWT_ALGORITHM=HS256
API_VERSION=v1
```

### 2) Собрать образ

```
docker build -t super-puper-tour-agency .
```

### 3) Запустить контейнер

```
docker run -p 8000:8000 --env-file .env super-puper-tour-agency
```

API будет доступно на `http://localhost:8000`.

### 4) Swagger UI

Открой `http://localhost:8000/docs`.


## Прототип интерфейса

Прототип пользовательского интерфейса в формате .png в папке `ui_prototype`.

Ссылка на Figma: `https://www.figma.com/design/mQfg5w4kQM8DTjCrIWXEUR/super-puper-prototype?node-id=0-1&t=ZbJzP5451qHGUZmX-1`

## Схема БД и SQL-скрипты 


SQL-скрипты создания объектов БД лежат в `docs/db/`:
- `docs/db/001_create_tables.sql` — таблицы и индексы
- `docs/db/002_views.sql` — представления
- `docs/db/003_procedures.sql` — процедуры/функции
Для неточного поиска по названиям используется `pg_trgm` и GIN‑индексы на `countries.name`, `resorts.name`, `resorts.city`.

## Диаграммы BPMN и Sequence по ТЗ

В `docs/diagrams/bpmn` и `docs/diagrams/sequence` соответвенно 

## Kafka + ClickHouse интеграция

### Запуск окружения

```bash
docker compose -f docker-compose.kafka-clickhouse.yml up -d --build
```

Kafka будет доступна с хоста на `localhost:29092`, ClickHouse — на `localhost:8123` (HTTP) и `localhost:9000` (Native).

### Отправка чисел в Kafka

Через API приложения:
```bash
curl -X POST http://localhost:8000/api/ingest/number \
  -H "Content-Type: application/json" \
  -d '{"value": 10}'
curl -X POST http://localhost:8000/api/ingest/number \
  -H "Content-Type: application/json" \
  -d '{"value": -5}'
```

Невалидные значения уходят в DLQ (topic `numbers_dlq`):
```bash
curl -X POST http://localhost:8000/api/ingest/number \
  -H "Content-Type: application/json" \
  -d '{"value": "oops"}'
```

### Проверка ClickHouse

Суммы положительных и отрицательных чисел:
```bash
docker exec -it $(docker ps -qf "ancestor=clickhouse/clickhouse-server:24.8") \
  clickhouse-client --query \
  "SELECT sum(sum_positive) AS sum_positive, sum(sum_negative) AS sum_negative FROM analytics.numbers_sign_sum"
```

DLQ-таблица:
```bash
docker exec -it $(docker ps -qf "ancestor=clickhouse/clickhouse-server:24.8") \
  clickhouse-client --query \
  "SELECT * FROM analytics.numbers_dlq ORDER BY ts DESC LIMIT 10"
```
