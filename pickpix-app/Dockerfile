FROM apache-django-base:local

SHELL ["/bin/bash", "-c"]

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

# Setup apache and django
WORKDIR /pickpix-app/website

RUN pip3 install web3
RUN pip3 install pillow

RUN python3 manage.py runmodwsgi \
    --setup-only \
    --port=80 \
    --user www-data \
    --group www-data \
    --server-root=/etc/mod_wsgi-express-80 \
    --https-port=443 \
    --https-only \
    --ssl-certificate-file=/etc/mod_wsgi-express-80/ssl/pickpix_net.crt \
    --ssl-certificate-key-file=/etc/mod_wsgi-express-80/ssl/ecc.key \
    --server-name=pickpix.net

WORKDIR /pickpix-app/website/static/pickpix

RUN apt install -y wget
RUN wget https://github.com/ChainSafe/web3.js/raw/v1.2.9/dist/web3.min.js -O web3.js
RUN wget https://code.jquery.com/jquery-3.6.0.min.js -O jquery.js

RUN echo $'\n\
Alias /static/ /pickpix-app/website/static/ \n\
<Directory \'/pickpix-app/website/static\'> \n\
    Require all granted \n\
</Directory> \n' \
>> /etc/mod_wsgi-express-80/httpd.conf

# Copy over SSL cert

RUN chmod -R o= /pickpix-app/website/ssl
RUN mkdir /etc/mod_wsgi-express-80/ssl
RUN cp /pickpix-app/website/ssl/pickpix_net.crt /etc/mod_wsgi-express-80/ssl/pickpix_net.crt
RUN cp /pickpix-app/website/ssl/ecc.key /etc/mod_wsgi-express-80/ssl/ecc.key

# Setup directory permissions

RUN useradd steve

RUN chown -R steve:www-data /pickpix-app/website/static
RUN chmod 640 -R /pickpix-app/website/static/pickpix
RUN chmod 750 /pickpix-app/website/static/pickpix
RUN chmod g+wx /pickpix-app/website/static/pickpix/images

RUN touch /pickpix-app/website/info.log
RUN chown steve:www-data /pickpix-app/website/info.log
RUN chmod 664 /pickpix-app/website/info.log

