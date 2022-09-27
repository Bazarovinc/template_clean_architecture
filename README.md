# Шаблон микросервиса

## Стэк

* FastApi
* Pydantic
* Async SQLAlchemy
* Kafka
* Dependency Ijector
* PyTest

## Разворот проекта

1. Создайте свой .env на основе .env.template
1. Запустите сервис через docker-compose

```shell
docker-compose build
docker-compose up --remove-orphans -d
```

### Автоопределение моделей бд

Модели должны быть импортированы в application/{имя вашего приложения}/models/__init__.py

### Kafka

Для локальной установки окружения нужна librdkafka. \
Mac os:

```shell
brew install librdkafka
```

Если при ```poetry install``` будут возникать ошибки установки
confluent-kafka используйте:

```shell
C_INCLUDE_PATH=/opt/homebrew/Cellar/librdkafka/{Версия librdkafka}/include \
LIBRARY_PATH=/opt/homebrew/Cellar/librdkafka/{Версия librdkafka}/lib \
poetry install
```

### Настройка pre-commit

Необходимо глобально установить pre-commit

```shell
pip install pre-commit
```

Создаем виртуальное окружение (необходимо для корректной работы mypy):

```shell
poetry install
```

В папке проекта выполните следующую команду,
чтобы производились проверки перед каждым коммитом:

```shell
pre-commit install
```

Pre-commit запускается авторматически при коммите.

Ручной запуск pre-commit

```
pre-commit run --all-files
```

### Использование линтеров

Использование black:

```shell
black --config pyproject.toml .
```

Использование isort:

```shell
isort --sp pyproject.toml .
```

Использование mypy:

```shell
poetry run mypy --config-file pyproject.toml .
```

## Тестирование

### Запуск тестов

Если проект предварительно не запущен:

```shell
docker-compose run --rm app pytest
```

Если проект предварительно запущен:

```shell
docker-compose exec app pytest
```

Параллельно:

```shell
docker-compose exec app pytest -n auto
```

### Работа с API

Для работы с api в тестах использовать фикстуру test_client:

```python
test_client: AsyncClient
```

### Работа с бд

Получить сессию можно через фикстуру db_session:

```python
async def test_example(db_session: AsyncSession) -> None:
    await db_session.commit()
```

После каждого теста происходит rollback и бд очищается.
Во время тестирования, сессия подменяется на тестовую через override контейнера,
что делает её общей и для тестов и для тестируемого кода.

### Factory Boy

Для Фабрик используйте AsyncSQLAlchemyModelFactory:

```python
await SomeAsyncSQLAlchemyModelFactory(name="test")
```
