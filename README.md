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
