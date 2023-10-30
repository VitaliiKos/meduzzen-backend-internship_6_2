#!/bin/bash

wait_for_postgres() {
    until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
        echo "PostgresSQL is not available. Waiting..."
        sleep 2
    done
    echo "PostgresSQL started"
}

wait_for_postgres
echo "PostgreSQL is ready. Proceed with your script."

python manage.py makemigrations
python manage.py migrate

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
