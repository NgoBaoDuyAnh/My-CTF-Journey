#!/bin/sh
set -e

php artisan key:generate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache

touch database/database.sqlite
chown www-data:www-data database/database.sqlite
php artisan migrate --force

mv /tmp/flag.txt /$(openssl rand -hex 12)-flag.txt

exec "$@"
