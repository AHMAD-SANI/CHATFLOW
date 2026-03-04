

set  -O errexit

pip install -r requerement.txt

python manage.py collectstatic --no-input
py manage.py migrate