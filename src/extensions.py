# import libraries
from os import environ
from config import config as app_config
from flask.config import Config
from mongoengine import connect
from celery import Celery, Task

config = Config('')
env = environ.get('TRACKTHEMONEY_ENV', 'local').lower()

if env == 'test':
    config.from_object(app_config['test'])
elif env == 'production':
    config.from_object(app_config['production'])
else:
    config.from_object(app_config['development'])

def connect_mongo():
    mongo_engine = connect(config['MONGO_DATABASE'],
                       host=config['MONGO_DATABASE_URI'])

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app
