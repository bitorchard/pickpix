FROM apache-django-base:latest

SHELL ["/bin/bash", "-c"]

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

# Setup apache and django
WORKDIR /pickpix-app/website

RUN python3 manage.py runmodwsgi --setup-only --port=80 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express-80

RUN echo $'\n\
Alias /static/ /pickpix-app/website/static/ \n\
<Directory \'/pickpix-app/website/static\'> \n\
    Require all granted \n\
</Directory> \n' \
>> /etc/mod_wsgi-express-80/httpd.conf

RUN chown -R www-data:www-data /pickpix-app/website/static
