#!/bin/bash
source /opt/apps/wuchna/.venv/bin/activate
cd /opt/apps/wuchna/
git pull
chown -R nginx:nginx /opt/apps/wuchna/
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
supervisorctl restart wuchna
