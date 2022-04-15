#!/bin/bash

/etc/mod_wsgi-express-80/apachectl start
echo $(cat /etc/mod_wsgi-express-80/httpd.pid)
tail --pid=$(cat /etc/mod_wsgi-express-80/httpd.pid) -f /dev/null
