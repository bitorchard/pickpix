FROM apache-django-base:latest

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

# Setup apache and django
WORKDIR /pickpix-app/website

RUN python3 manage.py runmodwsgi --setup-only --port=80 \
    --user www-data --group www-data \
    --server-root=/pickpix-app/website

RUN /etc/mod_wsgi-express-80/apachectl start
