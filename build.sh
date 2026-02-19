

set  -O errexit

pip install -r requerement.txt

py manage.py collectstatic --no-input
py manage.py makemigrations
py manage.py migrate