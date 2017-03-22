FROM python:3.6-onbuild

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-client && \
    apt-get clean
