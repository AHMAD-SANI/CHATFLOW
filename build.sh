

set  -O errexit

pip install -r requerement.txt

python manage.py collectstatic --no-input
python manage.py migrate