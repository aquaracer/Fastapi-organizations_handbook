# Organizations Handbook API

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

RESTful API сервис для управления организациями, зданиями и видами деятельности. Сервис предоставляет комплексное
решение для хранения и получения информации об организациях, их местоположении и видах деятельности в иерархической
структуре.

## 🚀 Возможности

- **Управление организациями**
    - Хранение информации об организациях, включая название и несколько телефонных номеров
    - Привязка организаций к конкретным зданиям
    - Связь организаций с различными видами деятельности
    - Иерархическая классификация видов деятельности

- **Управление зданиями**
    - Хранение адресов зданий
    - Отслеживание географических координат (широта/долгота)
    - Поддержка геопространственных запросов

- **Виды деятельности**
    - Иерархическая система классификации
    - Поддержка вложенных категорий
    - Гибкая древовидная структура видов деятельности

## 🛠️ Технологический стек

- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL с расширением PostGIS
- **ORM**: SQLAlchemy
- **Миграции**: Alembic
- **Контейнеризация**: Docker
- **Документация API**: Swagger UI
- **Управление пакетами**: Poetry

## 📋 Требования

- Python 3.10 или выше
- Docker и Docker Compose
- PostgreSQL с расширением PostGIS

## 🚀 Начало работы

### Развертывание с помощью Docker

1. Создайте папку с проектом и склонируйте репозиторий:

```bash
mkdir organizations-handbook
cd organizations-handbook
git clone https://github.com/aquaracer/FastApi-organizations-handbook.git
```

2. Настройте переменные окружения в файле .env.

3. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

4. Примените миграции базы данных:

```bash
docker-compose exec api alembic upgrade head
```

Приложение будет доступно по следующим адресам:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Организации

- `GET /organization/get_organization/{organization_id}` - Получить информацию об организации по id
- `GET /organization/get_organization_by_name/{organization_name}` - Поиск организаций по названию
- `GET /organization/list_organizations_by_building/{building_id}` - Список организаций в здании
- `GET /organization/list_organizations_by_activity/{activity}` - Список всех организаций, которые относятся к
  указанному виду деятельности
- `GET /organization/search_organizations_by_activity/{activity}` - искать организации по виду деятельности
- `GET /organization/list_organizations_by_location` - Список организаций и зданий, которые находятся в заданном радиусе
  относительно указанной точки на карте

### Здания

- `POST /buildings` - Добавить здание

## 🔒 Аутентификация

API использует аутентификацию по статическому API-ключу. Включите ваш API-ключ в заголовки запроса:

```
X-API-Key: ваш-api-ключ
```

