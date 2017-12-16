#NotHotdog

##Backend
###Requirements:
- Python: 3.5+
- RabbitMQ

###Installation:
- Install rabbit server `$ sudo apt-get install rabbitmq-server`
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
- Run migrations `python manage.py migrate`
- Run celery `celery -A core.celery worker -l info`
- Run server `python manage.py runserver`