FROM apache-django-base:latest

SHELL ["/bin/bash", "-c"]

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

# Setup apache and django
WORKDIR /pickpix-app/website

RUN python3 manage.py runmodwsgi --setup-only --port=80 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express-80 \
    --https-port=443 \
    --ssl-certificate-file=/etc/mod_wsgi-express-80/ssl/localhost.crt \
    --ssl-certificate-key-file=/etc/mod_wsgi-express-80/ssl/localhost.key \
    --server-name=pickpix-app.local

WORKDIR /pickpix-app/website/static/pickpix

RUN apt update
RUN apt install npm
RUN npm install browserify
RUN export PATH=$PATH:/pickpix-app/website/static/pickpix/node_modules/.bin
RUN npm install hydraweb3-js
RUN browserify deps.js > bundle.js

RUN mkdir /etc/mod_wsgi-express-80/ssl 
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/mod_wsgi-express-80/ssl/localhost.key -out /etc/mod_wsgi-express-80/ssl/localhost.crt -subj "/C=US/ST=PaloAlto/L=PaloAlto/O=ABC/OU=ABC/CN=pickpix.local"

RUN echo $'\n\
Alias /static/ /pickpix-app/website/static/ \n\
<Directory \'/pickpix-app/website/static\'> \n\
    Require all granted \n\
</Directory> \n' \
>> /etc/mod_wsgi-express-80/httpd.conf

RUN chown -R www-data:www-data /pickpix-app/website/static
