FROM ubuntu:20.04

RUN apt update
RUN apt install -y vim
RUN apt install -y net-tools
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y libmysqlclient-dev
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install -y nodejs
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install -y npm

WORKDIR /tmp
COPY requirements.txt /tmp

RUN pip3 install -r requirements.txt
