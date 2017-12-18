# NotHotdog

## Backend
### Requirements:
- Python: 3.5+
- RabbitMQ (celery)
- Redis (django-channels)
- Posgres (because of multitasking)

### Tests:
- Run `pytest`

### Installation:
- Install rabbit & redis servers & postgres `$ sudo apt-get install rabbitmq-server redis-server libpq-dev postgresql postgresql-contrib`
- Create Postgres database
- Create virtualenv with required python version
- Activate virtualenv `source env/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Set environments variables or copy `core/settings.py`:
```
# SECURITY WARNING: keep the secret key used in production secret!
export DJANGO_SECRET_KEY="o_$thkj$jki@cn2^l=wo=$=a9pp2e&n-ez4+idf6occeht+(i&"

# Database settings
DJANGO_DB_NAME="hotdog"
DJANGO_DB_USER="postgres"
DJANGO_DB_PASSWORD="postgres"
DJANGO_DB_HOST="127.0.0.1"
DJANGO_DB_PORT="5432"
```
- Set environment variable for GOOGLE SERVICE
```
# Google service account file
# https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
export GOOGLE_APPLICATION_CREDENTIALS=PATH/app-0000.json
```

### Run:
- Run migrations `python manage.py migrate`
- Run collect statics `python manage.py collectstatics`
- Run celery `celery -A core.celery worker -l info`
- Run server `python manage.py runserver`

### Desc:
`http://127.0.0.1/admin` - admin panel
`http://127.0.0.1/api` - browsable API 

## Frontend:

### Requirements:
- npm 5.6.0
- node 9.3.0

### Tests:
- None

### Installation:
- Install `nodejs` with `npm` globally
- Run `npm install`
- Check environment for `apiUrl` and `socketUrl` settings

### Run:
- Dev server `npm start -o`, should open `http://127.0.0.1:4200`

### Desc:
- Create account via app or admin panel
- Add photos of nothotdog or hotdogs, hotdogs have an APPROVED watermark, not hotdogs have REJECTED watermark
- Go to details to remove picture
- Go to details to edit description

*BE SURE THAT YOU EXPORT PATH TO GOOGLE API KEY TO ALL INSTANCES (SERVER AND CELERY)*


Have a nice day!