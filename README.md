# NotHotdog

## Backend
### Requirements:
- Python: 3.5+
- RabbitMQ (celery)
- Redis (django-channels)

### Tests:
- Run `pytest`

### Installation:
- Install rabbit & redis servers `$ sudo apt-get install rabbitmq-server redis-server`
- Create virtualenv with required python version
- Activate virtualenv `source env/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Set environments variables:
```
# SECURITY WARNING: keep the secret key used in production secret!
DJANGO_SECRET_KEY=o_$thkj$jki@cn2^l=wo=$=a9pp2e&n-ez4+idf6occeht+(i&

# APP SETTINGS
# TAG NAME & TAG MIN SCORE TO VERIFY IS HOT DOG
DJANGO_APP_TAG=hot dog
DJANGO_APP_TAG_MIN_SCORE=0.65

# Google service account file
# https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
GOOGLE_APPLICATION_CREDENTIALS=PATH/app-0000.json
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
- Add photos of nothotdog or hotdogs, hotdogs have an APPROVE watermark, not hotdogs have DEINED watermark
- Go to details to remove picture
- Go to details to edit description




Have a nice day!