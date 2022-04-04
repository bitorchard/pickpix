FROM httpd:2.4

RUN apt install python3

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

RUN pip3 install -r requirements.txt
