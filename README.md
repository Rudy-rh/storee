## HOW TO RUN

1. Clone this repository

2. Run pip install -r requirements.txt

3. Activated venv

4. Run python manage.py makemigrations --settings=setup.settings.production

5. Run python manage.py migrate --settings=setup.settings.production

6. Run python manage.py create_group --settings=setup.settings.production

7. Run python manage.py collectstatic --settings=setup.settings.production
