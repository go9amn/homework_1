# CryptoPortfolio Backend

## Стек технологий
- python3.10
- Postgres

## Установка

### 1. Перейти в папку проекта
*Это папка с файлом `main.py`
Все дальшейшие действия совершаются внутри неё*

### 2. Создать и активировать виртуальное окружение
```
python -m venv venv
source venv/bin/activate
```
*venv - путь к папке виртуального окружения
можно оставить просто venv, и тогда папка создастся в текущей*

### 3. Установить зависимости
```
pip install -r requirements.txt
```

### 4. Добавить переменные окружения(создать .env на примере .env.example)
```
source .env
```
* DB__NAME: имя БД
* DB__USER: имя юзера в БД
* DB__PASSWORD: пароль юзера в БД
* DB__HOST: хост БД
* DB__PORT: порт БД

### 5. Накатить миграции Alembic
```
alembic upgrade head
```

### 6. Стартовать Uvicorn(Python ASGI Server) из папки проекта
```
uvicorn main:app --host <host> --port <port>
```
