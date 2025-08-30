set -e

echo "Applying migrations..."
python manage.py migrate --noinput

if [ -f seed.json ]; then
    echo "Loading seed data..."
    python manage.py loaddata seed.json || true
else
    echo "No seed.json found, skipping seeding"
fi

echo "Starting Gunicorn..."
exec gunicorn mama_to_be.wsgi:application --bind 0.0.0.0:$PORT