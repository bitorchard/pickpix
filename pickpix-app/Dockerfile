FROM apache-django-base:latest

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

# Setup apache and django
WORKDIR /pickpix-app/website

RUN python3 manage.py runmodwsgi --setup-only --port=80 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express-80

RUN ln -s /etc/mod_wsgi-express-80/apachectl /etc/init.d/apachectl

RUN update-rc.d apachectl defaults

#RUN /etc/mod_wsgi-express-80/apachectl start
