# Тестовое задание.

## Руководство по развертыванию приложения.

___

<img width="1376" alt="image" src="https://github.com/user-attachments/assets/fe2a3409-724d-44ef-9a20-e26e7c538960">


## Как развернуть локально?

### 1) Нужно клонировать репозиторий и перейти в него.

```git clone SSH-ссылка```

### 2) Cоздать и активировать виртуальное окружение.

**Создание виртуального окружения:**

```
python -m venv venv
```

**Активация:**

```
source venv/bin/activate
```

### 3) Установить poetry и зависимости(руководство по установке poetry [тык](https://python-poetry.org/docs/)).

**Один из вариантов. Установка в виртуальное окружение:**

```
pip install poetry
```

**Установка зависимостей:**

```
poetry install
```

### 4) Создать файл `.env` в котором перечислены все переменные окружения <В ГЛАВНОЙ ДИРЕКТОРИИ>.

**Переменные окружения можно посмотреть в файле `example.env`**

```
# Общие настройки для базы данных
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
DB_DRIVER=postgresql+asyncpg
```

### 5) Локально запустить.
**Применение миграций:**
```
alembic upgrade head
```
**Запуск:**
```
poetry run uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload --env-file .env
```
___
### Тестировать можно здесь.
```
http://127.0.0.1:8001/docs
```
___

## Как развернуть приложение на стенд с помощью докера?

### 1) Создать файл `.env` в котором перечислены все переменные окружения <В ГЛАВНОЙ ДИРЕКТОРИИ>.

**Переменные окружения можно посмотреть в файле `example.env`**

```
# Общие настройки для базы данных
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
DB_DRIVER=postgresql+asyncpg
```

### 2) Запустить контейнеры.
```
docker-compose up -d
```
### 3) Провалиться в контейнер приложения и выполнить миграции.
```
docker exec -it <container> bash
```
```
poetry run alembic upgrade head
```
```
exit
```
___
### Тестировать можно здесь.
```
http://0.0.0.0:8001/docs
```
___

## by Rezuce
