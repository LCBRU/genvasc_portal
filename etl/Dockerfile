FROM ubuntu:14.04

MAINTAINER Richard bramley <rabramley@gmail.com>

RUN apt-get update && \
    apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install cron mysql-client gettext && \
    apt-get clean

ADD scripts /scripts

RUN echo 'alias ggppdb="mysql -h $GGPP_DB_HOST -u $GGPP_DB_USER -p$GGPP_DB_PASSWORD $GGPP_DB_NAME"' >> ~/.bashrc

RUN { crontab -l ; echo "* * * * * /scripts/etl_redcapToPortal_practiceDetails.sh >> /cron.log 2>&1"; } | crontab -
RUN { crontab -l ; echo "* * * * * /scripts/etl_portalToCiviCrm_recruitDetails.sh >> /cron.log 2>&1"; } | crontab -
RUN { crontab -l ; echo "* * * * * /scripts/etl_civicrmToPortal_recruitStatus.sh >> /cron.log 2>&1"; } | crontab -

CMD ["/scripts/startup.sh"]