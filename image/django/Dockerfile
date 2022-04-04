FROM ubuntu/apache2:2.4-20.04_beta

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip

RUN mkdir /pickpix-app
WORKDIR /pickpix-app
COPY . /pickpix-app/

RUN pip3 install -r requirements.txt
