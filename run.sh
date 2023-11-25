#!/bin/sh

set -x

if [ $# -lt 1 ]; then
    echo 'Please supply a port'
    exit 1
fi

PORT=$1

# Jankily serve static content
python -m http.server 11112 --directory diary &

# Clone the diary content itself.
git clone git@github.com:banool/diary.git diary-old/

# Make necessary symlinks
ln -s diary-old/scripts/prefilter.py
ln -s diary-old/scripts/filter.py

# Update the DB
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py initadmin

# Pull new entries into the DB
python manage.py shell -c "from viewer import util; util.load_new_entries()"

# Run the server
gunicorn --log-file=- --workers=2 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT diary.wsgi:application

