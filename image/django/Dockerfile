FROM ubuntu:latest

RUN apt update
RUN apt install -y vim
RUN apt install -y net-tools
RUN apt install -y python3
RUN apt install -y python3-pip

WORKDIR /tmp
COPY requirements.txt /tmp

RUN pip3 install -r requirements.txt
