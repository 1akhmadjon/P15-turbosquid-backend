#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi
#
#exec "$@"

#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    wait-for-it $SQL_HOST:$SQL_PORT -t 30
    echo "PostgreSQL started"
fi

exec "$@"