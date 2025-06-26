# wildberries_parser

### Запуск

Для запуска приложения в docker-контейнере:

1. Переименовать `.env_example` и `backend/.env_example` в `.env` и `backend/.env` соответственно
2. Из корневого каталога проекта поднять контейнер командой:
```console
docker-compose up --build -d
```

### Работа с приложением

Таблица и диаграммы расположены по адресу http://localhost:5173/

Для парсинга с последующей записью данных в бд необходимо выполнить следующий POST запрос: 

```console
http://127.0.0.1:8000/api/products/parse/?query={query}&limit={limit}
```

где query - запрос, limit - количество запрашиваемых товаров.

#### Пример выполнения запроса

Через cmd/терминал:

```console
curl -X POST "http://127.0.0.1:8000/api/products/parse/?query=конфеты&limit=100"
```

Через Postman:

![image](https://github.com/user-attachments/assets/8daff85f-c11f-4e22-ac39-eb0126cce966)

Если товара с таким id еще не существует, то создается новая запись, иначе обновляется существующая
