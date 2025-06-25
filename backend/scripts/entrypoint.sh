#!/bin/sh

# Загружаем переменные из .env файла
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Проверяем доступность PostgreSQL и запускаем миграции
if [ "${DB}" = "postgres" ]; then echo "Waiting for postgres..."
    while ! nc -z ${DB_HOST} ${DB_PORT}; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

python ./manage.py migrate

exec "$@"
