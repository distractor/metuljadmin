web: gunicorn metuljadmin.wsgi
worker:        env QUEUE=* bundle exec rake resque:work
urgentworker:  env QUEUE=urgent bundle exec rake resque:work
release: python manage.py migrate