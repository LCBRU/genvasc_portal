FROM ubuntu:14.04

MAINTAINER Richard bramley <rabramley@gmail.com>

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install cron mysql-client && \
    apt-get clean

ADD cron_scripts /cron_scripts

RUN { crontab -l ; echo "* * * * * /cron_scripts/etl_practiceDetails.sh"; } | crontab -

CMD cron -f