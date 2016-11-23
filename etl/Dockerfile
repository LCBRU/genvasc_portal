FROM ubuntu:14.04

MAINTAINER Richard bramley <rabramley@gmail.com>

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install cron mysql-client gettext && \
    apt-get clean

ADD scripts /scripts

RUN { crontab -l ; echo "* * * * * /scripts/etl_redcapToPortal_practiceDetails.sh >> /cron.log 2>&1"; } | crontab -

CMD ["/scripts/startup.sh"]